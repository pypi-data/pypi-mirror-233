#
# **************************************************************************
#
# simple_rep_fifo.py                                       (c) Spectrum GmbH
#
# **************************************************************************
#
# Example for all SpcMDrv based analog replay cards. 
# Shows a simple FIFO mode example using only the few necessary commands
#
# Information about the different products and their drivers can be found
# online in the Knowledge Base:
# https://www.spectrum-instrumentation.com/en/platform-driver-and-series-differences
#
# Feel free to use this source for own projects and modify it in any kind
#
# Documentation for the API as well as a detailed description of the hardware
# can be found in the manual for each device which can be found on our website:
# https://www.spectrum-instrumentation.com/en/downloads
#
# Further information can be found online in the Knowledge Base:
# https://www.spectrum-instrumentation.com/en/knowledge-base-overview
#
# **************************************************************************
#

import sys
import numpy as np
import spcm

# to speed up the calculation of new data we pre-calculate the signals
# to simplify that we use special frequencies
adSignalFrequency_Hz = [ 40000, 20000, 10000, 5000, 2500, 1250, 625, 312.5 ]

#
# **************************************************************************
# main 
# **************************************************************************
#

# open card
# uncomment the first line and replace the IP address to use remote
# cards like in a generatorNETBOX
# with spcm.Card('TCPIP::192.168.1.10::inst0::INSTR') as card:
with spcm.Card('/dev/spcm0') as card:
    if not card: sys.exit(-1)
    print("Driver version: {major}.{minor}.{build}".format(**card.drv_version()))

    # read type, function and sn and check for D/A card
    lCardType = card.get(spcm.SPC_PCITYP)
    lSerialNumber = card.sn()
    lFncType = card.get(spcm.SPC_FNCTYPE)

    sProductName = card.product_name()
    if lFncType == spcm.SPCM_TYPE_AO or lFncType == spcm.SPCM_TYPE_DO or lFncType == spcm.SPCM_TYPE_DIO:
        print("Found: {0} sn {1:05d}".format(sProductName, lSerialNumber))
    else:
        print("This is an example for analog output, digital output and digital I/O cards.\nCard: {0} sn {1:05d} not supported by example".format(sProductName, lSerialNumber))
        sys.exit(-1)


    # set samplerate to 1 MHz (M2i) or 50 MHz, no clock output
    if ((lCardType & spcm.TYP_SERIESMASK) == spcm.TYP_M4IEXPSERIES) or ((lCardType & spcm.TYP_SERIESMASK) == spcm.TYP_M4XEXPSERIES):
        card.sample_rate(spcm.MEGA(50))
    else:
        card.sample_rate(spcm.MEGA(1))
    card.set(spcm.SPC_CLOCKOUT, 0)

    # driver might have adjusted the sampling rate to the best-matching value, so we work with that value
    sample_rate = llSetSamplerate = card.get(spcm.SPC_SAMPLERATE)

    # set up the mode
    qwChEnable = spcm.CHANNEL0 | spcm.CHANNEL1
    # qwChEnable = spcm.CHANNEL0
    card.set_card_mode(spcm.SPC_REP_FIFO_SINGLE)
    card.set(spcm.SPC_CHENABLE, qwChEnable)

    num_channels     = card.get(spcm.SPC_CHCOUNT)
    bytes_per_sample = card.get(spcm.SPC_MIINST_BYTESPERSAMPLE)

    # setup software buffer
    notify_size_bytes = 1024 * 1024  # 1 MB
    notify_num_samples = notify_size_bytes // bytes_per_sample
    notify_size_bytes_per_channel = notify_size_bytes // num_channels
    notify_num_samples_per_channel = notify_num_samples // num_channels
    buffer_size_bytes = 32 * notify_size_bytes    # 32 MByte. For simplicity buffer_size_bytes should be a multiple of notify_size_bytes
    card.allocate_buffer(buffer_size_bytes)

    ## Precalculating the data
    print("Sample rate: {} S/s".format(sample_rate))
    print("Lowest used frequency: {} Hz".format(np.min(adSignalFrequency_Hz[:num_channels])))
    data_per_channel_length = int(sample_rate / np.min(adSignalFrequency_Hz[:num_channels]))
    print("Per channel number of precalculated points: {}".format(data_per_channel_length))
    data_total_length = buffer_size_bytes // bytes_per_sample
    data_total_length = np.int32(np.ceil(data_total_length / data_per_channel_length)*data_per_channel_length)
    data_per_channel_length = data_total_length // num_channels
    memory_size = data_total_length * bytes_per_sample # number of bytes
    print("Total number of precalculated points: {}".format(data_total_length))
    print("Memory usage of precalculated points: {}".format(memory_size))
    print("Notify size: {} Samples - {} Bytes".format(notify_num_samples, notify_size_bytes))
    data_range = np.arange(data_per_channel_length)
    data_matrix = np.empty((data_per_channel_length, num_channels), dtype=np.int16)
    for chan in range(num_channels):
        data_matrix[:, chan] = np.int16(32767 * np.sin(2.* np.pi*data_range/(llSetSamplerate / adSignalFrequency_Hz[chan])))
    data_matrix = data_matrix.ravel()
    print("Len: {} Buf: {}".format(data_total_length, data_matrix.shape))

    # setup the trigger mode
    # (SW trigger, no output)
    card.set(spcm.SPC_TRIG_ORMASK,      spcm.SPC_TMASK_SOFTWARE)
    card.set(spcm.SPC_TRIG_ANDMASK,     0)
    card.set(spcm.SPC_TRIG_CH_ORMASK0,  0)
    card.set(spcm.SPC_TRIG_CH_ORMASK1,  0)
    card.set(spcm.SPC_TRIG_CH_ANDMASK0, 0)
    card.set(spcm.SPC_TRIG_CH_ANDMASK1, 0)
    card.set(spcm.SPC_TRIGGEROUT,       0)

    # setup all channels
    for i in range(0, num_channels):
        card.out_amp(i, 1000)
        card.out_enable(i, 1)

    # calculate the data
    # we calculate data for all enabled channels, starting at sample position 0, and fill the complete DMA buffer
    current_sample_position = 0
    num_available_samples = (buffer_size_bytes // num_channels) // bytes_per_sample
    print("Number of available samples: {}".format(num_available_samples))
    indices = np.arange(num_available_samples)
    card.buffer[indices] = data_matrix[indices]
    current_sample_position += num_available_samples

    # we define the buffer for transfer and start the DMA transfer
    card.start_buffer_transfer(notify_size=notify_size_bytes)
    card.set(spcm.SPC_DATA_AVAIL_CARD_LEN, buffer_size_bytes)

    # We'll start the replay and run until a timeout occurs or user interrupts the program
    lStatus = 0
    user_len = 0
    user_pos = 0
    lFillsize = 0
    bStarted = False
    acRunIndicator = [ '.', 'o', 'O', 'o' ]
    lRunIndicatorIdx = 0
    try:
        while True:
            # dwError = 
            try:
                card.cmd(spcm.M2CMD_DATA_WAITDMA) # TODO Have to create a timeout mechanism
            except spcm.SpcmTimeout as timeout:
                print("... Timeout")
            # start the card if the onboard buffer has been filled completely
            lFillsize = card.get(spcm.SPC_FILLSIZEPROMILLE)
            if lFillsize == 1000 and bStarted is False:
                print("\n... data has been transferred to board memory")
                print("Starting the card...")
                try:
                    card.start(spcm.M2CMD_CARD_ENABLETRIGGER)
                except spcm.SpcmTimeout as timeout:
                    print("Timeout!")
                    break
                else:
                    bStarted = True
            else:
                # print the fill size and an indicator to show that the program is still running
                # change indicator every 25 loops to get nice update rate
                sys.stdout.write("\r... Fillsize: {0:d}/1000 {1}".format(lFillsize, acRunIndicator[lRunIndicatorIdx // 25]))
                lRunIndicatorIdx = (lRunIndicatorIdx + 1) % (len(acRunIndicator) * 25)

            lStatus = card.get(spcm.SPC_M2STATUS)
            user_len = card.get(spcm.SPC_DATA_AVAIL_USER_LEN)
            user_pos = card.get(spcm.SPC_DATA_AVAIL_USER_POS)

            # calculate new data
            if user_len >= notify_size_bytes:
                start_sample_buf_sample = user_pos // bytes_per_sample
                start_sample_pre_sample = current_sample_position % (data_total_length // 2)

                indices     = np.arange(start_sample_buf_sample, start_sample_buf_sample + notify_num_samples)
                pre_indices = np.arange(start_sample_pre_sample, start_sample_pre_sample + notify_num_samples)

                card.buffer[indices] = data_matrix[pre_indices]
                card.set(spcm.SPC_DATA_AVAIL_CARD_LEN, notify_size_bytes)
                current_sample_position += notify_num_samples
    except spcm.SpcmException as exception:
        # Probably a buffer underrun has happened, capure the event here
        print(exception)
        

    # send the stop command
    card.stop(spcm.M2CMD_DATA_STOPDMA)

