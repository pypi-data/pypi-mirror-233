# -*- coding: utf-8 -*-

from contextlib import ExitStack

from .regs import *
from .spcerr import *

from .classes import Device, Card, SpcmException, SpcmError, SpcmTimeout
from .classes_sync import Sync

from . import pyspcm

class CardStack(ExitStack):
    """A context manager object for handling multiple Card objects with or without a Sync object
 
    Parameters
    ----------
    cards : list <Card>
        a list of card objects that is managed by the context manager
    sync : Sync
        an object for handling the synchronization of cards
    
    Methods
    -------
    __bool__
        Checks if all the card object are connected and returns true if all connections are alive
    synched
        Checks if the sync card is connected
    """

    cards = []
    sync = None

    def __init__(self, card_identifiers = [], sync_identifier = None) -> None:
        super().__init__()
        # Handle card objects
        self.cards = [self.enter_context(Card(identifier)) for identifier in card_identifiers]
        if sync_identifier:
            self.sync = self.enter_context(Sync(sync_identifier))
        pass
        # super().__init__(*args, **kwargs)
    
    def __bool__(self) -> bool:
        """Checks if all defined cards are connected
        
        """
        connected = True
        for card in self.cards:
            connected &= bool(card)
        return connected
    
    def synched(self):
        """Checks if the sync card is connected
        """
        return bool(self.sync)
    
    @staticmethod
    def discover(dwMaxNumRemoteCards = 50, dwMaxVisaStringLen = 256, dwMaxIdnStringLen = 256, dwTimeout_ms = 5000) -> object:
        """Do a discovery of the cards connected through a network

        Returns
        -------
        CardStack
            a stack object with all the discovered cards
        """

        pszVisa = (pyspcm.c_char_p * dwMaxNumRemoteCards)()
        for i in range(0, dwMaxNumRemoteCards, 1):
            pszVisa[i] = pyspcm.cast(pyspcm.create_string_buffer(dwMaxVisaStringLen), pyspcm.c_char_p)
        pyspcm.spcm_dwDiscovery (pszVisa, pyspcm.uint32(dwMaxNumRemoteCards), pyspcm.uint32(dwMaxVisaStringLen), pyspcm.uint32(dwTimeout_ms))

        # ----- check from which manufacturer the devices are -----
        pszIdn = (pyspcm.c_char_p * dwMaxNumRemoteCards)()
        for i in range(0, dwMaxNumRemoteCards, 1):
            pszIdn[i] = pyspcm.cast(pyspcm.create_string_buffer(dwMaxIdnStringLen), pyspcm.c_char_p)
        pyspcm.spcm_dwSendIDNRequest (pszIdn, pyspcm.uint32(dwMaxNumRemoteCards), pyspcm.uint32(dwMaxIdnStringLen))

        # ----- store VISA strings for all discovered cards and open them afterwards -----
        listsSpectrumDevices = []
        for (id, visa) in zip(pszIdn, pszVisa):
            if not id:
                break

            if id.decode('utf-8').startswith("Spectrum GmbH,"):
                listsSpectrumDevices.append(visa.decode("utf-8"))
        
        return CardStack(card_identifiers=listsSpectrumDevices)