#
# **************************************************************************
#
# simple_rep_single.py                                     (c) Spectrum GmbH
#
# **************************************************************************
#
# Example for all SpcMDrv based analog replay cards as well as digital output
# and digital I/O cards. 
# Shows a simple standard mode example using only the few necessary commands
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
import spcm
# from ctypes import *

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

    # set up the mode
    if lFncType == spcm.SPCM_TYPE_AO:
        qwChEnable = 1
    else:
        qwChEnable = 0xFFFFFFFF  # enable 32 channels
    llMemSamples = spcm.KILO_B(64)
    llLoops = 0  # loop continuously
    card.set_card_mode(spcm.SPC_REP_STD_CONTINUOUS)
    card.set(spcm.SPC_CHENABLE,    qwChEnable)
    card.set(spcm.SPC_MEMSIZE,     llMemSamples)
    card.set(spcm.SPC_LOOPS,       llLoops)

    lSetChannels = card.get(spcm.SPC_CHCOUNT)
    lBytesPerSample = card.get(spcm.SPC_MIINST_BYTESPERSAMPLE)

    # setup the trigger mode
    # (SW trigger, no output)
    card.set(spcm.SPC_TRIG_ORMASK,      spcm.SPC_TMASK_SOFTWARE)

    # set up the analog output channels
    if lFncType == spcm.SPCM_TYPE_AO:
        lChannel = 0
        card.out_amp(lChannel, 1000) # 1000 mV
        card.out_enable(lChannel, 1)

    # setup software buffer
    if lFncType == spcm.SPCM_TYPE_AO:
        qwBufferSize = llMemSamples * lBytesPerSample * lSetChannels
    else:
        qwBufferSize = llMemSamples * lSetChannels // 8  # eight channels per byte for DO and DIO cards

    # allocate memory for data transfer
    card.allocate_buffer(buffer_size=qwBufferSize)
    # calculate the data
    if lFncType == spcm.SPCM_TYPE_AO:
        max_value = card.get(spcm.SPC_MIINST_MAXADCVALUE)
        # simple ramp for analog output cards
        for i in range(llMemSamples):
            card.buffer[i] = i % max_value
    else:
        # a tree for digital output cards
        for i in range(llMemSamples):
            card.buffer[i:i+1] = 0x1 << (i % 32) # TODO check if this works

    card.start_buffer_transfer(spcm.M2CMD_DATA_WAITDMA) # Wait for the writing to buffer being done

    # We'll start and wait until the card has finished or until a timeout occurs
    card.timeout(10000) # 10 s
    print("Starting the card and waiting for ready interrupt\n(continuous and single restart will have timeout)")
    try:
        card.start(spcm.M2CMD_CARD_ENABLETRIGGER, spcm.M2CMD_CARD_WAITREADY)
    except spcm.SpcmTimeout as timeout:
        print(timeout)
        print("-> Exiting")


