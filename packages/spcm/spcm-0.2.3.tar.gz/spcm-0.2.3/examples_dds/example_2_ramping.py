"""EXAMPLE 2 - Use the ramping functionality to do a long and slow frequency sweep 
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
    # Trigger changes every 2.0 seconds
    period_s = 2.0 # seconds
    card.trg_src(spcm.SPCM_DDS_TRG_SRC_TIMER)
    card.trg_timer(period_s)
    # For slow ramps only change the value every 1000 steps
    card.freq_ramp_stepsize(1000)
    card.amp_ramp_stepsize(1000)

    # Create one carrier and keep on for 2 seconds
    card.amp(0, 0.1)
    card.freq(0, 100e6) # Hz
    card.exec_at_trg()

    # Ramp the frequency of the carrier
    card.frequency_slope(0, 300e6 / period_s) # 150 MHz/s
    card.exec_at_trg()

    # Stop frequency ramp
    card.frequency_slope(0, 0)
    card.freq(0, 400e6) # 400 MHz
    card.exec_at_trg()

    # Ramp the amplitude of the carrier
    card.amplitude_slope(0, -0.09 / period_s) # 1/s
    card.exec_at_trg()

    # Stop amplitude ramp
    card.amplitude_slope(0, 0)
    card.amp(0, 0.01)
    card.exec_at_trg()

    ## Write the list of commands to the card
    card.write_to_card()

    # Start the card
    card.start()