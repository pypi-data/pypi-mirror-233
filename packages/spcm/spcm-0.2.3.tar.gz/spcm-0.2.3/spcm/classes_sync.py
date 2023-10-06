# -*- coding: utf-8 -*-

from .regs import *
from .spcerr import *

from . import pyspcm, spcm_tools

from .classes import Device

class Sync(Device):
    """a class to control Spectrum Instrumentation Starhub synchronization devices

    For more information about what setups are available, please have a look at the user manual
    for your specific Starhub.

    Parameters
    ----------
    

    Methods
    ----------
    

    Exceptions
    ----------
    SpcmException
    SpcmTimeout
    """

    def enable_mask(self, mask : int) -> None:
        """Enable channels on the Starthub using a bit mask

        Parameters
        ----------
        mask : int
            bit mask that turns-on specific StartHub channels
        """

        self.set(SPC_SYNC_ENABLEMASK, mask)
    
    def clock_mask(self, mask : int) -> None:
        """Enable the clock signal sharing on the StarHub using a bit mask

        Parameters
        ----------
        mask : int
            bit mask that turns-on clock sharing on specific StarHub channels
        """
        
        self.set(SPC_SYNC_CLKMASK, mask)