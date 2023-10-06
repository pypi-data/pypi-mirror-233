"""EXAMPLE 5 - Do FM and AM on several carriers at the same time
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
    card.write_to_card()
    
    ## Setup DDS
    card.dds_reset()

    ## Start the DDS test
    card.connections(spcm.SPCM_DDS_CONN_CORE1_TO_CORE0_AM | spcm.SPCM_DDS_CONN_CORE2_TO_CORE0_FM)
    card.trg_src(spcm.SPCM_DDS_TRG_SRC_NONE)
    # Create one carrier and keep on for 2 seconds
    card.amp(0, 0.1)
    card.freq(0, 100.0e6) # 100 MHz
    # Amplitude modulation is done with core 1 on core 0
    card.amp(1, 0.5)
    card.freq(1, 2) # 2 Hz
    # Frequency modulation is done with core 2 on core 1
    card.freq(2, 1) # 1 Hz
    card.amp(2, 50e6) # 50 MHz

    card.exec_now()
    card.write_to_card()

    # Start the card
    card.start()
