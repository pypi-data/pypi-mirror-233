#
# **************************************************************************
#
# simple_rec_single.py                                      (c) Spectrum GmbH
#
# **************************************************************************
#
# Example for all SpcMDrv based analog acquisition cards. 
#
# Information about the different products and their drivers can be found
# online in the Knowledge Base:
# https://www.spectrum-instrumentation.com/en/platform-driver-and-series-differences
#
# Shows a simple Standard mode example using only the few necessary commands
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

# import spectrum driver functions
import spcm
import sys
import numpy as np

#
# **************************************************************************
# main 
# **************************************************************************
#

# szErrorTextBuffer = create_string_buffer(ERRORTEXTLEN)
# dwError = uint32()


# open card
# uncomment the first line and replace the IP address to use remote
# cards like in a digitizerNETBOX
# with spcm.Card('TCPIP::192.168.1.10::inst0::INSTR') as card:
with spcm.Card('/dev/spcm0') as card:
    if not card: sys.exit(-1)
    print("Driver version: {major}.{minor}.{build}".format(**card.drv_version()))

    # read type, function and sn and check for A/D card
    lCardType = card.get(spcm.SPC_PCITYP)
    lSerialNumber = card.sn()
    lFncType = card.get(spcm.SPC_FNCTYPE)
    sCardName = card.product_name()
    if lFncType == spcm.SPCM_TYPE_AI:
        print("Found: {0} sn {1:05d}\n".format(sCardName, lSerialNumber))
    else:
        print("This is an example for A/D cards.\nCard: {0} sn {1:05d} not supported by example\n".format(sCardName, lSerialNumber))
        sys.exit(1)

    # determine the number of channels on the card
    lNumModules = card.get(spcm.SPC_MIINST_MODULES)
    lNumChPerModule = card.get(spcm.SPC_MIINST_CHPERMODULE)
    lNumChOnCard = lNumModules * lNumChPerModule

    # set memsize to 16 kiS
    lNumSamples = spcm.KIBI(16)

    # do a simple standard setup
    card.set(spcm.SPC_CHENABLE,       (1 << lNumChOnCard) - 1)  # enable all channels on card
    card.set(spcm.SPC_MEMSIZE,        lNumSamples)                 # acquire 16 kiS in total
    card.set(spcm.SPC_POSTTRIGGER,    lNumSamples // 2)            # half of the total number of samples after trigger event
    card.set_card_mode(spcm.SPC_REC_STD_SINGLE)       # single trigger standard mode
    card.timeout(5000)                     # timeout 5 s
    card.set(spcm.SPC_TRIG_ORMASK,    spcm.SPC_TMASK_SOFTWARE)       # trigger set to software
    card.set(spcm.SPC_TRIG_ANDMASK,   0)                        # ...
    card.set(spcm.SPC_CLOCKMODE,      spcm.SPC_CM_INTPLL)            # clock mode internal PLL

    lSetChannels = card.get(spcm.SPC_CHCOUNT)         # get the number of activated channels
    channels_list = range(0, lSetChannels, 1)
    
    # set up the channels
    for lChannel in channels_list:
        card.out_amp(lChannel, 1000)  # set input range to +/- 1000 mV

    # we try to set the samplerate to 100 kHz (M2i) or 20 MHz on internal PLL, no clock output
    card.sample_rate(spcm.MEGA(20))

    # define the data buffer
    card.allocate_buffer(num_samples=lNumSamples)

    # Start DMA transfer
    card.start_buffer_transfer(direction=spcm.SPCM_DIR_CARDTOPC)
    
    # start card
    card.start(spcm.M2CMD_CARD_ENABLETRIGGER, spcm.M2CMD_DATA_WAITDMA)

    # Reshape data
    alMin = np.min(card.buffer, axis=1)
    alMax = np.max(card.buffer, axis=1)

    print("Finished...\n")
    for lChannel in range(0, lSetChannels, 1):
        print("Channel {0:d}".format(lChannel))
        print("\tMinimum: {0:d}".format(alMin[lChannel]))
        print("\tMaximum: {0:d}".format(alMax[lChannel]))


