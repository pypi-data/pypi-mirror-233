"""EXAMPLE 6 - External Trigger
"""

import sys
import spcm

## Load the card
with spcm.DDS('/dev/spcm0') as card:
    if not card: sys.exit(-1)
    print("Driver version: {major}.{minor}.{build}".format(**card.drv_version()))
    
    ## Setup the card
    num_channels = 2
    card.set(spcm.SPC_CHENABLE, (0x1 << num_channels) - 1) # enable all channels
    for channel_index in range(num_channels):
        card.out_enable(channel_index, True)
        card.out_amp(channel_index, 1000)
    
    # Activate external trigger mode
    card.set(spcm.SPC_TRIG_EXT0_ACDC, 0) # set DC coupling
    card.set(spcm.SPC_TRIG_ORMASK, spcm.SPC_TMASK_EXT0) # disable default software trigger
    card.set(spcm.SPC_TRIG_ANDMASK, spcm.SPC_TMASK_NONE) # Enable external trigger within the AND mask
    card.set(spcm.SPC_TRIG_EXT0_LEVEL0, 1500) # Trigger level is 1.5 V (1500 mV)
    card.set(spcm.SPC_TRIG_EXT0_MODE, spcm.SPC_TM_POS)
    card.write_to_card()
    
    ## Setup DDS
    card.dds_reset()

    ## Start the DDS test
    card.trg_src(spcm.SPCM_DDS_TRG_SRC_CARD)
    card.exec_at_trg()

    # Create one carrier and keep it off
    card.amp(0, 0)
    card.freq(0, 100e6) # 100 MHz
    card.exec_now()

    for i in range(100):
        card.amp(0, 0.25)
        card.exec_at_trg() # wait for trigger, then turn on
        card.amp(0, 0.0)
        card.exec_now()    # turn off as soon as possible again
    card.write_to_card()

	# Start the card
    card.start()
