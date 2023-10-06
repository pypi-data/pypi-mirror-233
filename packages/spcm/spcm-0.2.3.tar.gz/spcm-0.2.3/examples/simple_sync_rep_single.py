#
# **************************************************************************
#
# simple_sync_rep_single.py                                (c) Spectrum GmbH
#
# **************************************************************************
#
# Example for two synchronized SpcMDrv based analog replay cards.
# Shows a simple standard mode example using only the few necessary commands.
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

import spcm

# from pyspcm import *
# from spcm_tools import *
import sys
from math import sin
from math import pi

#
# **************************************************************************
# main 
# **************************************************************************
#

card_identifiers = ["/dev/spcm0", "/dev/spcm1"]
sync_identifier  = "sync0"

# open cards and sync
with spcm.CardStack(card_identifiers=card_identifiers, sync_identifier=sync_identifier) as stack:
    if not stack: sys.exit(-1)

    for card in stack.cards:
        # read function and sn and check for D/A card
        lSerialNumber = card.sn()
        lFncType = card.get(spcm.SPC_FNCTYPE)
        sCardName = card.product_name()
        if lFncType == spcm.SPCM_TYPE_AO:
            print("Found: {0} sn {1:05d}\n".format(sCardName, lSerialNumber))
        else:
            print("This is an example for D/A cards.\nCard: {0} sn {1:05d} not supported by this example\n".format(sCardName, lSerialNumber))
            sys.exit(1)

    # setup star-hub
    nCardCount = len(card_identifiers)
    stack.sync.enable_mask((1 << nCardCount) - 1)


    # do a simple setup in CONTINUOUS replay mode for each card
    llMemSamples = spcm.KIBI(64)
    llLoops = 0  # loop continuously
    i = 0
    for card in stack.cards:
        lCardType = card.get(spcm.SPC_PCITYP)
        lSerialNumber = card.sn()
        lFncType = card.get(spcm.SPC_FNCTYPE)
        # set samplerate to 1 MHz (M2i, M2p) or 50 MHz (M4i, M4x), no clock output
        if ((lCardType & spcm.TYP_SERIESMASK) == spcm.TYP_M4IEXPSERIES) or ((lCardType & spcm.TYP_SERIESMASK) == spcm.TYP_M4XEXPSERIES):
            card.set(spcm.SPC_SAMPLERATE, spcm.MEGA(50))
        else:
            card.set(spcm.SPC_SAMPLERATE, spcm.MEGA(1))
        card.set(spcm.SPC_CLOCKOUT,   0)

        # calculate the number of channels on this card
        lNumModules = card.get(spcm.SPC_MIINST_MODULES)
        lNumChPerModule = card.get(spcm.SPC_MIINST_CHPERMODULE)
        lNumChOnCard = lNumModules * lNumChPerModule

        # set up the mode
        card.set_card_mode(spcm.SPC_REP_STD_CONTINUOUS)
        card.set(spcm.SPC_CHENABLE,    (1 << lNumChOnCard) - 1)  # enable all channels
        card.set(spcm.SPC_MEMSIZE,     llMemSamples)
        card.set(spcm.SPC_LOOPS,       llLoops)

        lSetChannels = card.get(spcm.SPC_CHCOUNT)
        lBytesPerSample = card.get(spcm.SPC_MIINST_BYTESPERSAMPLE)

        # setup the trigger mode
        # (SW trigger, no output)
        lFeatures = card.get(spcm.SPC_PCIFEATURES)
        if lFeatures & (spcm.SPCM_FEAT_STARHUB5 | spcm.SPCM_FEAT_STARHUB16):
            # set star-hub carrier card as clock master and trigger master
            card.set(spcm.SPC_TRIG_ORMASK,  spcm.SPC_TMASK_SOFTWARE)
            stack.sync.clock_mask(1 << i)
        else:
            card.set(spcm.SPC_TRIG_ORMASK,  spcm.SPC_TMASK_NONE)
        card.set(spcm.SPC_TRIG_ANDMASK,     0)
        card.set(spcm.SPC_TRIG_CH_ORMASK0,  0)
        card.set(spcm.SPC_TRIG_CH_ORMASK1,  0)
        card.set(spcm.SPC_TRIG_CH_ANDMASK0, 0)
        card.set(spcm.SPC_TRIG_CH_ANDMASK1, 0)
        card.set(spcm.SPC_TRIGGEROUT,       0)

        # set up the channels
        for lChannel in range(0, lSetChannels, 1):
            card.out_enable(lChannel, 1)
            card.out_amp(lChannel, 1000)

        # setup software buffer
        qwBufferSize = llMemSamples * lBytesPerSample * lSetChannels
        # we try to use continuous memory if available and big enough
        card.allocate_buffer(qwBufferSize)

        lMaxDACValue = card.get(spcm.SPC_MIINST_MAXADCVALUE)
        lMaxDACValue = lMaxDACValue - 1

        # calculate the data
        if i == 0: 
            # first card, generate a sine on each channel
            for lSampleIdx in range(0, llMemSamples, 1):
                for lChIdx in range(0, lSetChannels, 1):
                    dFactor = sin(2 * pi * lSampleIdx / (llMemSamples / (lChIdx + 1)))
                    card.buffer[lSampleIdx*lSetChannels + lChIdx] = int(lMaxDACValue * dFactor)
        elif i == 1:
            # second card, generate a rising ramp on each channel
            for lSampleIdx in range(0, llMemSamples, 1):
                for lChIdx in range(0, lSetChannels, 1):
                    dFactor = lSampleIdx / (llMemSamples / (lChIdx + 1))
                    card.buffer[lSampleIdx*lSetChannels + lChIdx] = int(lMaxDACValue * dFactor)
        elif i == 2:
            # third card, generate a rectangle on each channel
            for lSampleIdx in range(0, llMemSamples, 1):
                for lChIdx in range(0, lSetChannels, 1):
                    if lSampleIdx < ((llMemSamples / 2) / (lChIdx + 1)):
                        dFactor = 1
                    else:
                        dFactor = -1
                    card.buffer[lSampleIdx*lSetChannels + lChIdx] = int(lMaxDACValue * dFactor)
        elif i == 3:
            # fourth card, generate a falling ramp on each channel
            for lSampleIdx in range(0, llMemSamples, 1):
                for lChIdx in range(0, lSetChannels, 1):
                    dFactor = 1.0 - lSampleIdx / (llMemSamples / (lChIdx + 1))
                    card.buffer[lSampleIdx*lSetChannels + lChIdx] = int(lMaxDACValue * dFactor)
            
        # we define the buffer for transfer and start the DMA transfer
        card.start_buffer_transfer()

        card.timeout(10000)

        i += 1


    # We'll start and wait until the card has finished or until a timeout occurs
    # since the card is running in SPC_REP_STD_CONTINUOUS mode with SPC_LOOPS = 0 we will see the timeout
    try:
        stack.sync.start(spcm.M2CMD_CARD_ENABLETRIGGER, spcm.M2CMD_CARD_WAITREADY)
    except spcm.SpcmTimeout as timeout:
        stack.sync.stop()

