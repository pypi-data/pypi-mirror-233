"""EXAMPLE 3 - Tweezers

Ramping 20 carriers from a one setting to another
"""

import sys
import spcm
import numpy as np

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
    num_freq = 20
    first_init_freq_Hz  =  96e6 #  96 MHz
    last_init_freq_Hz   = 104e6 # 104 MHz
    first_final_freq_Hz =  99e6 #  99 MHz
    last_final_freq_Hz  = 101e6 # 101 MHz

    init_freq_Hz = np.linspace(first_init_freq_Hz, last_init_freq_Hz, num_freq)
    final_freq_Hz = np.linspace(first_final_freq_Hz, last_final_freq_Hz, num_freq)
    delta_freq_Hz = final_freq_Hz - init_freq_Hz

    # STEP 0 - Initialize frequencies
    card.trg_timer(2.0)
    card.trg_src(spcm.SPCM_DDS_TRG_SRC_TIMER)
    for i, freq in enumerate(init_freq_Hz):
        card.amp(i, 0.45 / num_freq)
        card.freq(i, freq)
    card.exec_at_trg()
    card.write_to_card()

    # STEP 1 - Start the ramp
    period_s = 5.0 # seconds
    card.trg_timer(period_s) # after 2.0 s stop the ramp
    for i, delta_Hz in enumerate(delta_freq_Hz):
        card.frequency_slope(i, delta_Hz / period_s) # Hz/s
    card.exec_at_trg()
    
    # STEP 2 - Stop the ramp
    for i, delta_Hz in enumerate(delta_freq_Hz):
        card.frequency_slope(i, 0) # Hz/s
        card.freq(i, final_freq_Hz[i])
    card.exec_at_trg()
    card.write_to_card()

    # Start the card
    card.start()
