"""spcm is a general Python package to control Spectrum Instrumentation GmbH PCIe-cards

...

Classes
----------
Card : (interface) class
    a class to control the low-level API interface of Spectrum Instrumentation cards
DDS : class
    child class of Card that specifically controls the DDS specific part of the card firmware
SpcmError : class
    all the errors that are raise by the low-level driver are packed into objects of this class
    and handled through exceptions

Exceptions
----------
SpcmException : (interface) class
    the main class to control exceptions that are raised due to errors that are raised 
    by the low-level driver.

    
Attributes
----------
see the files 'regs.py' and 'spcerr.py' for an extensive list of all the register names and
errors that are handled by the driver. For more information, please have a look at our
hardware specific user manuals.

Dependencies
----------
numpy

"""

# Import all registery entries and spectrum card errors into the module's name space
from .regs import *
from .spcerr import *
from .pyspcm import SPCM_DIR_PCTOCARD, SPCM_DIR_CARDTOPC, SPCM_BUF_DATA, SPCM_BUF_ABA, SPCM_BUF_TIMESTAMP

from .classes import Device, Card, SpcmError, SpcmException, SpcmTimeout
from .classes_dds import DDS
from .classes_sync import Sync
from .classes_card_stack import CardStack