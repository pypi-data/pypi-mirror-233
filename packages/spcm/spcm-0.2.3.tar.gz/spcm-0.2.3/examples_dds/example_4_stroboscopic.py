"""EXAMPLE 4 - Stroboscopic

Use one carrier to jump between different frequencies and create 
several time-averaged signals
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
    num_freq      = 100
    start_freq_Hz =  85.0e6 #  85 MHz
    end_freq_Hz   = 115.0e6 # 115 MHz
    
    freq_list = np.linspace(start_freq_Hz, end_freq_Hz, num_freq)

    # STEP 0 - Initialize frequencies
    period_s = 1.0 # seconds
    card.trg_src(spcm.SPCM_DDS_TRG_SRC_TIMER)
    card.trg_timer(period_s)
    card.amp(0, 0.45)
    card.freq(0, freq_list[0])
    card.exec_at_trg()
    card.write_to_card()
    
    # STEP 1a - Pre-fill Buffer
    period_s = 10e-5 # 100 us
    card.trg_timer(period_s)
    dds_fill_max = card.get(spcm.SPC_DDS_QUEUE_CMD_MAX)
    print(dds_fill_max)
    fill_number = int(dds_fill_max / 2)
    print(fill_number)
    for column in range(fill_number):
        frequency = freq_list[column % num_freq]
        card.freq(0, frequency)
        card.exec_at_trg()
    card.write_to_card()
    print(card.get(spcm.SPC_DDS_QUEUE_CMD_COUNT))

    ## Start the card
    card.start()

    # STEP 1b - Streaming data points
    print(dds_fill_max)
    dds_fill_count = card.get(spcm.SPC_DDS_QUEUE_CMD_COUNT)
    print(dds_fill_count)
    while True: # infinitely long streaming
        while True:
            dds_fill_count = card.get(spcm.SPC_DDS_QUEUE_CMD_COUNT)
            if dds_fill_count < dds_fill_max / 4: break
        for column in range(fill_number):
            frequency = freq_list[column % num_freq]
            card.freq(0, frequency)
            card.exec_at_trg()
        card.write_to_card()
        dds_status = card.get(spcm.SPC_DDS_STATUS)
        if dds_status & spcm.SPCM_DDS_STAT_QUEUE_UNDERRUN:
            break

    print("ERROR: Buffer underrun")