#
# **************************************************************************
#
# simple_rep_sequence.py                                   (c) Spectrum GmbH
#
# **************************************************************************
#
# Example for all SpcMDrv based analog replay cards. 
# Shows a simple sequence mode example using only the few necessary commands
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
from enum import IntEnum

import msvcrt
from time import sleep

USING_EXTERNAL_TRIGGER = False
LAST_STEP_OFFSET = 0


def lKbhit():
    return ord(msvcrt.getch()) if msvcrt.kbhit() else 0

#
#**************************************************************************
# vWriteSegmentData: transfers the data for a segment to the card's memory
#**************************************************************************
#

def vWriteSegmentData (card : spcm.Card, num_active_channels : int, segment_index : int, segment_len_sample : int):
    bytes_per_sample = 2
    segment_len_bytes = segment_len_sample * bytes_per_sample * num_active_channels

    # setup
    card.set(spcm.SPC_SEQMODE_WRITESEGMENT, segment_index)
    card.set(spcm.SPC_SEQMODE_SEGMENTSIZE,  segment_len_sample)

    # write data to board (main) sample memory
    card.start_buffer_transfer(spcm.M2CMD_DATA_WAITDMA, notify_size=0, transfer_length=segment_len_bytes)


#
# **************************************************************************
# DoDataCalculation: calculates and writes the output data for all segments
# **************************************************************************
#

# (main) sample memory segment index:
class SEGMENT_IDX(IntEnum):
    SEG_RAMPUP   =  0  # ramp up
    SEG_RAMPDOWN =  1  # ramp down
    SEG_SYNC     =  2  # negative sync puls, for example oscilloscope trigger
    #                       3 // unused
    SEG_Q1SIN    =  4  # first quadrant of sine signal
    SEG_Q2SIN    =  5  # second quadrant of sine signal
    SEG_Q3SIN    =  6  # third quadrant of sine signal
    SEG_Q4SIN    =  7  # fourth quadrant of sine signal
    SEG_STOP     =  8  # DC level for stop/end


def vDoDataCalculation(card : spcm.Card, card_type, num_active_channels, max_value):
    segment_len_sample = 0
    segment_len_byte   = 0

    print("Calculation of output data")


    factor = 1
    # This series has a slightly increased minimum size value.
    if ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M4IEXPSERIES) or ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M4XEXPSERIES) or ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M5IEXPSERIES):
        factor = 6

    # buffer for data transfer
    segment_len_byte = 2 * factor * 512 * num_active_channels  # max value taken from sine calculation below

    card.allocate_buffer(buffer_size = segment_len_byte)

    # helper values: Full Scale
    full_scale = max_value
    half_scale = full_scale // 2

    # !!! to keep the example simple we will generate the same data on all active channels !!!

    # data for the channels is interleaved. This means that we first write the first sample for each
    # of the active channels into the buffer, then the second sample for each channel, and so on
    # Please see the hardware manual, chapte "Data organization" for more information

    # to generate different signals on all channels:
    # for i in range(0, dwSegmentLenSample, 1):
    #    for ch in range(0, lNumActiveChannels, 1):
    #        if ch == 0:
    #            # generate a sine wave on channel 0
    #            card.buffer[i * lNumActiveChannels + ch] = int16 (dwFS * math.sin(2.0 * math.pi * (i / dwSegmentLenSample) + 0.5))
    #        elif ch == 1:
    #            # generate a ramp on ch1
    #            card.buffer[i * lNumActiveChannels + ch] = int16 (i * dwFS // dwSegmentLenSample)
    #        elif ch == 2:
    #            ...
    #
    # using numpy.column_stack is another possibility to interleave the data

    # --- sync puls: first half zero, second half -FS
    segment_len_sample = factor * 80
    for i in range(0, segment_len_sample // 2, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = 0
    for i in range(segment_len_sample // 2, segment_len_sample, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = -max_value

    vWriteSegmentData(card, num_active_channels, SEGMENT_IDX.SEG_SYNC, segment_len_sample)

    # --- ramp up
    segment_len_sample = factor * 64
    for i in range(0, segment_len_sample, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = i * half_scale // segment_len_sample

    vWriteSegmentData(card, num_active_channels, SEGMENT_IDX.SEG_RAMPUP, segment_len_sample)

    # --- ramp down
    segment_len_sample = factor * 64
    for i in range(0, segment_len_sample, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = full_scale - (i * half_scale // segment_len_sample)

    vWriteSegmentData(card, num_active_channels, SEGMENT_IDX.SEG_RAMPDOWN, segment_len_sample)

    # sine
    # write each quadrant in an own segment
    # --- sine, 1st quarter
    segment_len_sample = factor * 128
    for i in range(0, segment_len_sample, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = half_scale + int(half_scale * np.sin(2.0 * np.pi * (i + 0*segment_len_sample) / (segment_len_sample * 4)) + 0.5)
    vWriteSegmentData(card, num_active_channels, SEGMENT_IDX.SEG_Q1SIN, segment_len_sample)

    # --- sine, 2nd quarter
    segment_len_sample = factor * 128
    for i in range(0, segment_len_sample, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = half_scale + int(half_scale * np.sin(2.0 * np.pi * (i + 1*segment_len_sample) / (segment_len_sample * 4)) + 0.5)
    vWriteSegmentData(card, num_active_channels, SEGMENT_IDX.SEG_Q2SIN, segment_len_sample)

    # --- sine, 3rd quarter
    segment_len_sample = factor * 128
    for i in range(0, segment_len_sample, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = half_scale + int(half_scale * np.sin(2.0 * np.pi * (i + 2*segment_len_sample) / (segment_len_sample * 4)) + 0.5)
    vWriteSegmentData(card, num_active_channels, SEGMENT_IDX.SEG_Q3SIN, segment_len_sample)

    # --- sine, 4th quarter
    segment_len_sample = factor * 128
    for i in range(0, segment_len_sample, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = half_scale + int(half_scale * np.sin(2.0 * np.pi * (i + 3*segment_len_sample) / (segment_len_sample * 4)) + 0.5)
    vWriteSegmentData(card, num_active_channels, SEGMENT_IDX.SEG_Q4SIN, segment_len_sample)


    # --- DC level
    segment_len_sample = factor * 128
    for i in range(0, segment_len_sample, 1):
        for ch in range(0, num_active_channels, 1):
            card.buffer[i * num_active_channels + ch] = full_scale // 2
    vWriteSegmentData(card, num_active_channels, SEGMENT_IDX.SEG_STOP, segment_len_sample)


#
#**************************************************************************
# vWriteStepEntry
#**************************************************************************
#

def vWriteStepEntry(card, step_index, step_next_index, segment_index, loops, flags):
    qwSequenceEntry = 0

    # setup register value
    qwSequenceEntry = (flags & ~spcm.SPCSEQ_LOOPMASK) | (loops & spcm.SPCSEQ_LOOPMASK)
    qwSequenceEntry <<= 32
    qwSequenceEntry |= ((step_next_index << 16) & spcm.SPCSEQ_NEXTSTEPMASK) | (int(segment_index) & spcm.SPCSEQ_SEGMENTMASK)

    card.set(spcm.SPC_SEQMODE_STEPMEM0 + step_index, qwSequenceEntry)



#
# **************************************************************************
# vConfigureSequence
# **************************************************************************
#

def vConfigureSequence(card):
    # sequence memory
    # four sequence loops are programmed (each with 6 steps)
    # a keystroke or ext. trigger switched to the next sequence
    # the loop value for the ramp increase in each sequence
    #  0 ...  5: sync, Q1sin, Q2sin, Q3sin, Q4sin, ramp up
    #  8 ... 13: sync, Q2sin, Q3sin, Q4sin, Q1sin, ramp down
    # 16 ... 21: sync, Q3sin, Q4sin, Q1sin, Q2sin, ramp up
    # 24 ... 29: sync, Q4sin, Q1sin, Q2sin, Q3sin, ramp down

                          #  +-- StepIndex
                          #  |   +-- StepNextIndex
                          #  |   |  +-- SegmentIndex
                          #  |   |  |                          +-- Loops
                          #  |   |  |                          |   +-- Flags: SPCSEQ_ENDLOOPONTRIG
    #  sine               #  |   |  |                          |   |          For using this flag disable Software-Trigger above.
    vWriteStepEntry (card,  0,  1, SEGMENT_IDX.SEG_SYNC,      3,  0)
    vWriteStepEntry (card,  1,  2, SEGMENT_IDX.SEG_Q1SIN,     1,  0)
    vWriteStepEntry (card,  2,  3, SEGMENT_IDX.SEG_Q2SIN,     1,  0)
    vWriteStepEntry (card,  3,  4, SEGMENT_IDX.SEG_Q3SIN,     1,  0)
    vWriteStepEntry (card,  4,  5, SEGMENT_IDX.SEG_Q4SIN,     1,  0)
    if USING_EXTERNAL_TRIGGER == False:
        vWriteStepEntry (card,  5,  1,  SEGMENT_IDX.SEG_RAMPDOWN,  1,  0)
    else:
        vWriteStepEntry (card,  5,  8,  SEGMENT_IDX.SEG_RAMPDOWN,  1,  spcm.SPCSEQ_ENDLOOPONTRIG)
    # all our sequences come in groups of five segments
    global LAST_STEP_OFFSET
    LAST_STEP_OFFSET = 5

    # cosine
    vWriteStepEntry (card,  8,  9, SEGMENT_IDX.SEG_SYNC,      3,  0)
    vWriteStepEntry (card,  9, 10, SEGMENT_IDX.SEG_Q2SIN,     1,  0)
    vWriteStepEntry (card, 10, 11, SEGMENT_IDX.SEG_Q3SIN,     1,  0)
    vWriteStepEntry (card, 11, 12, SEGMENT_IDX.SEG_Q4SIN,     1,  0)
    vWriteStepEntry (card, 12, 13, SEGMENT_IDX.SEG_Q1SIN,     1,  0)
    if USING_EXTERNAL_TRIGGER == False:
        vWriteStepEntry (card, 13,  9,  SEGMENT_IDX.SEG_RAMPUP,    2,  0)
    else:
        vWriteStepEntry (card, 13, 16,  SEGMENT_IDX.SEG_RAMPUP,    2,  spcm.SPCSEQ_ENDLOOPONTRIG)

    # inverted sine
    vWriteStepEntry (card, 16, 17, SEGMENT_IDX.SEG_SYNC,      3,  0)
    vWriteStepEntry (card, 17, 18, SEGMENT_IDX.SEG_Q3SIN,     1,  0)
    vWriteStepEntry (card, 18, 19, SEGMENT_IDX.SEG_Q4SIN,     1,  0)
    vWriteStepEntry (card, 19, 20, SEGMENT_IDX.SEG_Q1SIN,     1,  0)
    vWriteStepEntry (card, 20, 21, SEGMENT_IDX.SEG_Q2SIN,     1,  0)
    if USING_EXTERNAL_TRIGGER == False:
        vWriteStepEntry (card, 21, 17,  SEGMENT_IDX.SEG_RAMPDOWN,  3,  0)
    else:
        vWriteStepEntry (card, 21, 24,  SEGMENT_IDX.SEG_RAMPDOWN,  3,  spcm.SPCSEQ_ENDLOOPONTRIG)

    # inverted cosine
    vWriteStepEntry (card, 24, 25, SEGMENT_IDX.SEG_SYNC,      3,  0)
    vWriteStepEntry (card, 25, 26, SEGMENT_IDX.SEG_Q4SIN,     1,  0)
    vWriteStepEntry (card, 26, 27, SEGMENT_IDX.SEG_Q1SIN,     1,  0)
    vWriteStepEntry (card, 27, 28, SEGMENT_IDX.SEG_Q2SIN,     1,  0)
    vWriteStepEntry (card, 28, 29, SEGMENT_IDX.SEG_Q3SIN,     1,  0)
    vWriteStepEntry (card, 29, 30, SEGMENT_IDX.SEG_RAMPUP,    4,  0)
    vWriteStepEntry (card, 30, 30, SEGMENT_IDX.SEG_STOP,      1,  spcm.SPCSEQ_END)  # M2i: only a few sample from this segment are replayed
                                                                       # M4i: the complete segment is replayed

    # Configure the beginning (index of first seq-entry to start) of the sequence replay.
    card.set(spcm.SPC_SEQMODE_STARTSTEP, 0)

    if False:
        print("\n")
        for i in range(0, 32, 1):
            llTemp = card.get(spcm.SPC_SEQMODE_STEPMEM0 + i)
            print("Step {0:.2}: 0x{1:016llx}\n".format(i, llTemp))

        print("\n\n")


#
# **************************************************************************
# main 
# **************************************************************************
#

# open card
# uncomment the second line and replace the IP address to use remote
# cards like in a generatorNETBOX
# with spcm.Card('TCPIP::192.168.1.10::inst0::INSTR') as card:
with spcm.Card('/dev/spcm0') as card:
    if not card: sys.exit(-1)
    print("Driver version: {major}.{minor}.{build}".format(**card.drv_version()))


    # read type, function and sn and check for D/A card
    card_type = card.get(spcm.SPC_PCITYP)
    sn = card.sn()
    function_type = card.get(spcm.SPC_FNCTYPE)

    product_name = card.product_name()
    if function_type == spcm.SPCM_TYPE_AO:
        print("Found: {0} sn {1:05d}".format(product_name, sn))
    else:
        print("This is an example for D/A cards.\nCard: {0} sn {1:05d} not supported by example".format(product_name, sn))
        exit(-1)

    # set up the mode
    channels_enable = spcm.CHANNEL0
    # llChEnable = int64(CHANNEL0 | CHANNEL1)  # uncomment to enable two channels
    max_segments = 32
    card.set(spcm.SPC_CARDMODE,            spcm.SPC_REP_STD_SEQUENCE)
    card.set(spcm.SPC_CHENABLE,            channels_enable)
    card.set(spcm.SPC_SEQMODE_MAXSEGMENTS, max_segments)

    # set up trigger
    card.set(spcm.SPC_TRIG_ORMASK,      spcm.SPC_TMASK_SOFTWARE)  # software trigger
    card.set(spcm.SPC_TRIG_ANDMASK,     0)
    card.set(spcm.SPC_TRIG_CH_ORMASK0,  0)
    card.set(spcm.SPC_TRIG_CH_ORMASK1,  0)
    card.set(spcm.SPC_TRIG_CH_ANDMASK0, 0)
    card.set(spcm.SPC_TRIG_CH_ANDMASK1, 0)
    card.set(spcm.SPC_TRIGGEROUT,       0)

    # set up the channels
    num_channels = card.get(spcm.SPC_CHCOUNT)
    for channel_index in range(0, num_channels, 1):
        card.out_enable(channel_index, 1)
        card.out_amp(channel_index, 1000)
        card.set(spcm.SPC_CH0_STOPLEVEL + channel_index * (spcm.SPC_CH1_STOPLEVEL - spcm.SPC_CH0_STOPLEVEL), spcm.SPCM_STOPLVL_HOLDLAST)

    # set samplerate to 1 MHz (M2i) or 50 MHz, no clock output
    card.set(spcm.SPC_CLOCKMODE, spcm.SPC_CM_INTPLL)
    if ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M4IEXPSERIES) or ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M4XEXPSERIES):
        card.set(spcm.SPC_SAMPLERATE, spcm.MEGA(50))
    else:
        card.set(spcm.SPC_SAMPLERATE, spcm.MEGA(1))
    card.set(spcm.SPC_CLOCKOUT,   0)

    # generate the data and transfer it to the card
    max_value = card.get(spcm.SPC_MIINST_MAXADCVALUE)
    vDoDataCalculation(card, card_type, num_channels, max_value - 1)
    print("... data has been transferred to board memory")

    # define the sequence in which the segments will be replayed
    vConfigureSequence(card)
    print("... sequence configured\n")

    # We'll start and wait until all sequences are replayed.
    card.set(spcm.SPC_TIMEOUT, 0)
    print("Starting the card")
    card.start(spcm.M2CMD_CARD_ENABLETRIGGER)

    print("sequence replay runs, switch to next sequence (3 times possible) with")
    if USING_EXTERNAL_TRIGGER is False:
        print(" key: c ... change sequence")
    else:
        print(" a (slow) TTL signal on external trigger input connector")
    print(" key: ESC ... stop replay and end program")

    card_status = 0
    sequence_actual = 0    # first step in a sequence
    sequence_next = 0
    sequence_status_old = 0

    while True:
        key = lKbhit()
        if key == 27:  # ESC
            card.stop()
            break

        elif key == ord('c') or key == ord('C'):
            if USING_EXTERNAL_TRIGGER is False:
                sequence_next = ((sequence_actual + 8) % 32)
                print("sequence {0:d}\n".format(sequence_next // 8))

                # switch to next sequence
                # (before it is possible to overwrite the segment data of the new used segments with new values)
                step = 0

                # --- change the next step value from the sequence end entry in the actual sequence
                step = card.get(spcm.SPC_SEQMODE_STEPMEM0 + sequence_actual + LAST_STEP_OFFSET)
                step = (step & ~spcm.SPCSEQ_NEXTSTEPMASK) | (sequence_next << 16)
                card.set(spcm.SPC_SEQMODE_STEPMEM0 + sequence_actual + LAST_STEP_OFFSET, step)

                sequence_actual = sequence_next
        else:
            sleep(0.01)  # 10 ms

            # Demonstrate the two different sequence status values at M2i and M4i / M2p cards.
            sequence_status = card.get(spcm.SPC_SEQMODE_STATUS)

            # print the status only when using external trigger to switch sequences
            if USING_EXTERNAL_TRIGGER:
                if sequence_status_old != sequence_status:
                    sequence_status_old = sequence_status

                    if ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M2ISERIES) or ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M2IEXPSERIES):  # M2i, M2i-exp
                        if sequence_status & spcm.SEQSTAT_STEPCHANGE:
                            print("status: sequence changed\n")
                    if ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M4IEXPSERIES) or ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M4XEXPSERIES) or ((card_type & spcm.TYP_SERIESMASK) == spcm.TYP_M2PEXPSERIES):  # M4i, M4x, M2p
                        # Valid values only at a startet card available.
                        if card_status & spcm.M2STAT_CARD_PRETRIGGER:
                            print("status: actual sequence number: {0:d}\n".format(sequence_status))

        # end loop if card reports "ready" state, meaning that it has reached the end of the sequence
        card_status = card.get(spcm.SPC_M2STATUS)
        if (card_status & spcm.M2STAT_CARD_READY) != 0:
            break


