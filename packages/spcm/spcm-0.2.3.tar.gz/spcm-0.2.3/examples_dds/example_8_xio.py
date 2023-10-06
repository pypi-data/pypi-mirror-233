"""EXAMPLE 8 - XIO usage
"""

import sys
import spcm

## Load the card
card : spcm.DDS
with spcm.DDS('/dev/spcm0') as card:
    if not card: sys.exit(-1)
    print("Driver version: {major}.{minor}.{build}".format(**card.drv_version()))
    
    ## Setup the card
    num_channels = 2
    card.set(spcm.SPC_CHENABLE, (0x1 << num_channels) - 1) # enable all channels
    for channel_index in range(num_channels):
        card.out_enable(channel_index, True)
        card.out_amp(channel_index, 1000)
    
    # Activate the xio dds mode
    card.set(spcm.SPCM_X0_MODE, spcm.SPCM_XMODE_DDS);
    card.set(spcm.SPCM_X1_MODE, spcm.SPCM_XMODE_DDS);
    card.set(spcm.SPCM_X2_MODE, spcm.SPCM_XMODE_DDS);
    card.write_to_card()
    
    ## Setup DDS
    card.dds_reset()

    ## Start the DDS test
    card.trg_src(spcm.SPCM_DDS_TRG_SRC_TIMER)
    card.trg_timer(0.1) # 100 ms
    card.exec_at_trg()

    # Create one carrier and keep it off
    card.amp(0, 1.0)
    card.freq(0, 1e1) # 10 Hz

    card.dds_x_mode(0, spcm.SPCM_DDS_XMODE_MANUAL)
    card.dds_x_mode(1, spcm.SPCM_DDS_XMODE_WAITING_FOR_TRG)
    card.dds_x_mode(2, spcm.SPCM_DDS_XMODE_EXEC)

    card.x_manual_output(0x1)
    card.trg_timer(1.0) # s
    card.exec_at_trg()

    card.amp(0, 0.0)
    card.x_manual_output(0x0)
    card.exec_at_trg()
    card.write_to_card()

	# Start the card
    card.start()
