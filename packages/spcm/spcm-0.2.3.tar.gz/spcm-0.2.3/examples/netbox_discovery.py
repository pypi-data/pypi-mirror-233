#
# **************************************************************************
#
# netbox_discovery.py                                      (c) Spectrum GmbH
#
# **************************************************************************
#
# This example will send a LXI discovery request to the network and check the
# answers for Spectrum products.
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
from ctypes import *
import sys
import functools
from collections import namedtuple

# custom compare function for "Card" named tuples
def card_compare(lhs, rhs):
    if lhs.sIP < rhs.sIP:
        return -1
    elif lhs.sIP == rhs.sIP:
        # use "greater than" here to get the card with the Netbox-SN to the top
        if lhs.lNetboxSN > rhs.lNetboxSN:
            return -1
        elif lhs.lNetboxSN == rhs.lNetboxSN:
            if lhs.lCardSN < rhs.lCardSN:
                return -1
    return 1

# use a named tuple to simplify access to members
Card = namedtuple ("Card", "sIP lCardSN lNetboxSN sName sVISA sNetbox")

#
# **************************************************************************
# main
# **************************************************************************
#

with spcm.CardStack.discover() as stack:
    # ----- try to open each VISA string and read the Netbox SN if open was successful -----
    listCards = []
    for card in stack.cards:
        if not card: sys.exit(-1)
        # print("Driver version: {major}.{minor}.{build}".format(**card.drv_version()))

        # VISA string has format "TCPIP[x]::<IP>::instX::INSTR"
        # extract the IP from the VISA string
        sIP = card.device_identifier
        sIP = sIP[sIP.find('::') + 2:]
        sIP = sIP[:sIP.find ('::')]

        card_type = card.get(spcm.SPC_PCITYP)
        serial_number = card.sn()
        lNetboxType = card.get(spcm.SPC_NETBOX_TYPE)
        lNetboxSN = card.get(spcm.SPC_NETBOX_SERIALNO)
        product_name = card.product_name()

        sNetbox = ""
        if lNetboxType != 0:
            sNetbox = "DN{:x}.".format((lNetboxType & spcm.NETBOX_SERIES_MASK) >> 24)
            sNetbox += "{:x}".format  ((lNetboxType & spcm.NETBOX_FAMILY_MASK) >> 16)
            sNetbox += "{:x}".format  ((lNetboxType & spcm.NETBOX_SPEED_MASK) >> 8)
            sNetbox += "-{:d}".format  (lNetboxType & spcm.NETBOX_CHANNEL_MASK)

        listCards.append(Card(sIP, serial_number, lNetboxSN, product_name, card.device_identifier, sNetbox))

    # sort the list with the discovered cards because the order of answers to discovery is not defined
    listCards.sort(key=functools.cmp_to_key(card_compare))

    # ----- print the discovered Netboxes -----
    if listCards:
        print("Netboxes found:")

        sLastIP = ""
        for card in listCards:
            if card.sIP != sLastIP:
                print(f'{card.sNetbox} at {card.sIP} with SN {card.lNetboxSN}')
                sLastIP = card.sIP

            print(f'\t{card.sName} SN: {card.lCardSN} at {card.sVISA}')
    else:
        print("No Netboxes found!\n")
