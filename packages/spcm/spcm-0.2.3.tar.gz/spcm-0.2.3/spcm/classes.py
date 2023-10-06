# -*- coding: utf-8 -*-

import numpy as np
import traceback

from .regs import *
from .spcerr import *
from .pyspcm import SPCM_DIR_PCTOCARD, SPCM_DIR_CARDTOPC, SPCM_BUF_DATA, SPCM_BUF_ABA, SPCM_BUF_TIMESTAMP

from . import pyspcm, spcm_tools


class SpcmError():
    """a container class for handling driver level errors

    ...

    Methods
    ----------
    __init__(self, handle = None, register = None, value = None, text = None) -> None
        Constructs an error object, either by getting the last error from the card specified by the handle
        or using the information coming from the parameters register, value and text

        Parameters
        ----------
        handle : pyspcm.drv_handle (optional)
            a card handle to obtain the last error
        register, value and text : int, int, str (optional)
            parameters to define an error that is not raised by a driver error
        
        Examples
        ----------
        * error = SpcmError(handle=card.handle())
        * error = SpcmError(register=0, value=0, text="Some weird error")
    
    get_info(self) -> int
        gets the last error raised by the driver and puts it in specific class parameters

        Class parameters
        ----------
        * register
        * value
        * text

        Returns
        ----------
        The error code returned by the drivers error request
    
    __str__(self) -> str
        returns a human-readable string of the error, as contained in the parameter text
    
    Parameters
    ---------
    register : int
        the register address that triggered the error
    
    value : int
        the value that was written to the register address
    
    text : str
        the human-readable text associated with the error
    
    """

    register = None
    value = 0
    text = ""
    _handle = None
    
    def __init__(self, handle = None, register = None, value = None, text = None) -> None:
        if handle:
            self._handle = handle
            self.get_info()
        if register: self.register = register
        if value: self.value = value
        if text: self.text = text

    def get_info(self) -> int:
        """
        Gets the last error registered by the card and puts it in the object
    
        Class Parameters
        ----------
        self.register
        self.value
        self.text
    
        Returns
        -------
        int
            Error number of the spcm_dwGetErrorInfo_i32 class
        """

        register = pyspcm.uint32(0)
        value = pyspcm.int32(0)
        text = pyspcm.create_string_buffer(pyspcm.ERRORTEXTLEN)
        dwErr = pyspcm.spcm_dwGetErrorInfo_i32(self._handle, pyspcm.byref(register), pyspcm.byref(value), pyspcm.byref(text))
        self.register = register.value
        self.value = value.value
        self.text = text.value.decode('utf-8')
        return dwErr
    
    # TODO: should we add information about the register and value?
    def __str__(self) -> str:
        """
        Returns a human-readable text of the last error
    
        Class Parameters
        ----------
        self.register
        self.value
        self.text
    
        Returns
        -------
        str
            the human-readable text as saved in self.text.
        """
        
        return str(self.text)

class SpcmException(Exception):
    """a container class for handling driver level errors

    ...

    Methods
    ----------
    __init__(self, handle = None, register = None, value = None, text = None) -> None
        Constructs exception object and an associated error object, either by getting 
        the last error from the card specified by the handle or using the information 
        coming from the parameters register, value and text

        Parameters
        ----------
        handle : pyspcm.drv_handle (optional)
            a card handle to obtain the last error
        register, value and text : int, int, str (optional)
            parameters to define an error that is not raised by a driver error
        
        Examples
        ----------
        * raise SpcmException(handle=card.handle())
        * raise SpcmException(register=0, value=0, text="Some weird error")
    
    __str__(self) -> str
        returns a human-readable string of the error that is associated with this 
        exception
    
    Parameters
    ---------
    error : SpcmError
        the error that induced the raising of the exception
    
    """
    error = None
    def __init__(self, error = None, register = None, value = None, text = None) -> None:
        if error: self.error = error
        if register or value or text:
            self.error = SpcmError(register=register, value=value, text=text)
        
    
    def __str__(self) -> str:
        """
        Returns a human-readable text of the last error connected to the exception
    
        Class Parameters
        ----------
        self.error
    
        Returns
        -------
        str
            the human-readable text as return by the error
        """
        
        return str(self.error)

class SpcmTimeout(Exception):
    pass

class Device():
    """a class to control the low-level API interface of Spectrum Instrumentation devices

    For more information about what setups are available, please have a look at the user manual
    for your specific device.

    Parameters
    ----------
    
    device_identifier
        the identifying string that defines the used device

    Methods
    ----------
    __init__(self, device_identifier)
        Puts the device_identifier in the class parameter self.device_parameter

        Parameters
        ----------
        device_identifier : str
            an identifier string to connect to a specific device, for example:
            * Local PCIe device '/dev/spcm0'
            * Remote 'TCPIP::192.168.1.10::inst0::INSTR'

    __del__(self)
        Destructor that closes the connection associated with the handle

    __enter__(self)
        Constructs a handle using the parameter 'device_identifier', when using the with statement

    __exit__(self, _, error_value, _)
        Handles the exiting of the with statement, when either no code is left or an exception is thrown before

        Parameters
        ----------
        error_value : SpcmException
            Only this parameter is used and printed 
    
    __bool__(self)
        Truth value implementation of the class to check if a connection is active

        Examples
        -----------
        >>> card = spcm.Card('/dev/spcm0')
        >>> print(bool(card))
        <<< True # if a card was found at '/dev/spcm0'
    
    handle(self) -> pyspcm.drv_handle
        returns the active card handle
    
    drv_version(self)
        Get the version of the currently used driver

    cmd(self, cmd : int):
        send commands to the card using the register M2CMD.
    
    timeout(self, timeout : int)
        set the card timeout

    start(self)
        starts the active card
    
    stop(self)
        stop the active card
        
    reset(self)
        resets the active card

    write_setup(self):
        write the currently specified setup to the card.

    get(self, register : int) -> int
        gets the integer value of the specific register from the active card
    
    get_d(self, register : int) -> float
        gets the float value of the specific register from the active card
    
    set(self, register : int, value)
        sets the value of the specfic register to the active card

        Parameters
        ----------
        register : int
            all the different allowed registers are listed in the 'regs.py' file
        value : int/float
            the value that is written to the register
    
    get_error_info(self) -> SpcmError
        checks for the last error that was raised by the driver and return a SpcmError
        object with the specific information about the last error.
    
    print(self, text)
        prints text if the object has _verbose set
    
    Static Methods
    ----------
    open(device_identifier : str) -> pyspcm.drv_handle
        used the low-level driver to open a connection to a card identified by the 'device_identifier'
    
    close(handle : pyspcm.drv_handle) 
        closes the connection to card as specified by the handle

    Exceptions
    ----------
    SpcmException : (interface) class
        the main class to control exceptions that are raised due to errors that are raised 
        by the low-level driver. This exception is raised by the internal function 
        _check_error if the internal parameter _throw_error is True. All the get and set
        methods use the _check_error function to check for errors.
    SpcmTimeout : class
        an object signaling a timeout raised by the device
    """
    # public
    device_identifier = ""

    # private
    _last_error = None
    _handle = None
    _throw_error = True
    _verbose = True
    _closed = False

    def __init__(self, device_identifier : str) -> None:
        self.device_identifier = device_identifier
    
    def __del__(self) -> None:
        if not self._closed:
            self.stop()
            self._closed = True
            self.close(self._handle)

    def __enter__(self):
        # self._handle = self.open(self.device_identifier)
        self.open(self.device_identifier)
        if not self._handle and self._verbose:
            error = SpcmError(text="{} not found...".format(self.device_identifier))
            self.print(error)
            # raise SpcmException(error)
        return self
    
    def __exit__(self, exception, error_value, trace) -> None:
        if self._verbose and exception:
            self.print("Error type: {}".format(exception))
            self.print("Error value: {}".format(error_value))
            self.print("Traceback:")
            traceback.print_tb(trace)
        elif exception:
            self.print("Error: {}".format(error_value))
        self.stop()
        self._closed = True
        self.close(self._handle)
        if exception:
            raise exception
    
    def handle(self) -> pyspcm.drv_handle:
        """
        Returns the handle used by the object to connect to the active card
    
        Class Parameters
        ----------
        self._handle
    
        Returns
        -------
        pyspcm.drv_handle
            The active card handle
        """
        
        return self._handle

    # Check if a card was found
    def __bool__(self) -> bool:
        """
        Check for a connection to the active card
    
        Class Parameters
        ----------
        self._handle
    
        Returns
        -------
        bool
            True for an active connection and false otherwise
        """
        
        return bool(self._handle)
    
    ## High-level parameter functions, that use the low-level get and set function    
    def drv_version(self) -> dict:
        """
        Get the version of the currently used driver 

        Raises
        ------
        SpcmException
    
        Returns
        -------
        dict:
        - major
            the major version number (currently 6)
        - minor
            the minor version number (currently 5)
        - build
            the actual build
        
        """
        version_hex = self.get(SPC_GETDRVVERSION)
        major = (version_hex & 0xFF000000) >> 24
        minor = (version_hex & 0x00FF0000) >> 16
        build = version_hex & 0x0000FFFF
        version_dict = {"major": major, "minor": minor, "build": build}
        return version_dict

    def cmd(self, *args) -> None:
        """
        Execute spcm commands (e.g. M2CMD_CARD_WRITESETUP)

        Raises
        ------
        SpcmException
    
        Parameters
        ----------
        *args : int
            The differnt command flags to be executed.
        """

        cmd = 0
        for arg in args:
            cmd |= arg
        self.set(SPC_M2CMD, cmd)
    
    def timeout(self, timeout : int) -> None:
        """
        Sets the timeout
        
        Raises
        ------
        SpcmException
        """

        self.set(SPC_TIMEOUT, timeout)
    
    def start(self, *args) -> None:
        """
        Starts the connected card and enables triggering on the card

        Parameters
        ----------
        *args : int
            flags that are send together with the stop command
        
        Raises
        ------
        SpcmException
        """

        self.cmd(M2CMD_CARD_START, *args)
    
    def stop(self, *args : int) -> None:
        """
        Stops the connected card

        Parameters
        ----------
        *args : int
            flags that are send together with the stop command
            
            Flags
            -----
            M2CMD_DATA_STOPDMA
        
        Raises
        ------
        SpcmException
        """

        self.cmd(M2CMD_CARD_STOP, *args)
    
    def reset(self) -> None:
        """
        Resets the connected card
        
        Raises
        ------
        SpcmException
        """

        self.cmd(M2CMD_CARD_RESET)

    def write_setup(self, *args) -> None:
        """
        Writes of the configuration registers previously changed to the device

        Parameters
        ----------
        *args : int
            flags that are set with the write command

        Raises
        ------
        SpcmException
        """

        self.cmd(M2CMD_CARD_WRITESETUP, *args)
    
    ## Low-level get and set functions
    def get(self, register : str) -> int:
        """
        Get the integer value of a specific register of the card (see the user manual of your device)

        Raises
        ------
        SpcmException
    
        Parameters
        ----------
        register : int
            The specific register that will be read from.
        
        Returns
        -------
        int
            The value as stored in the specific register
        """

        self._check_closed()
        return_value = pyspcm.int64(0)
        dwErr = pyspcm.spcm_dwGetParam_i64(self._handle, register, pyspcm.byref(return_value))
        self._check_error(dwErr)
        return return_value.value
    
    def get_d(self, register : int) -> float:
        """
        Get the float value of a specific register of the card (see the user manual of your device)

        Raises
        ------
        SpcmException
    
        Parameters
        ----------
        register : int
            The specific register that will be read from.
        
        Returns
        -------
        float
            The value as stored in the specific register
        """

        self._check_closed()
        return_value = pyspcm.c_double(0)
        self._check_error(pyspcm.spcm_dwGetParam_d64(self._handle, register, pyspcm.byref(return_value)))
        return return_value.value

    def set(self, register : int, value) -> None:
        """
        Write the value of a specific register to the card (see the user manual of your device)

        Raises
        ------
        SpcmException
    
        Parameters
        ----------
        register : int
            The specific register that will be written.
        value : int or float
            The value that is written to the card. The function automatically detects whether a value is of integer or float type.
        """

        self._check_closed()
        if isinstance(value, (np.integer, int)):
            self._check_error(pyspcm.spcm_dwSetParam_i64(self._handle, register, value))
        elif isinstance(value, (np.floating, float)):
            self._check_error(pyspcm.spcm_dwSetParam_d64(self._handle, register, value))
        else:
            error = SpcmError()
            error.register = register
            error.value = value
            error.text = "Unknown value type: {} for register {} -> {}".format(type(value), register, value)
            raise SpcmException(error)

    ## Error handling and exception raising
    def _check_error(self, dwErr : int):
        """
        Create an SpcmError object and check for the last error

        Raises
        ------
        SpcmException
        SpcmTimeout
    
        Parameters
        ----------
        dwErr
            The error value as returned from a spcm_dwGetParam_* or spcm_dwSetParam_* call 
        """

        if dwErr not in [pyspcm.ERR_OK, pyspcm.ERR_TIMEOUT] and self._throw_error:
            self.get_error_info()
            raise SpcmException(self._last_error)
        elif dwErr == pyspcm.ERR_TIMEOUT:
            # self.print("Timeout!")
            raise SpcmTimeout("A card timeout occured")

    def get_error_info(self) -> SpcmError:
        """
        Create an SpcmError object and store it in an object parameter

        Raises
        ------
        SpcmException
    
        Returns
        ----------
        SpcmError
            the Error object containing the last error
        """

        self._last_error = SpcmError(self._handle)
        return self._last_error
    
    def _check_closed(self):
        """
        Check if a connection to the card exists and if not throw an error

        Raises
        ------
        SpcmException
    
        """
        if self._closed and self._throw_error:
            raise SpcmException(text="The connection to the card has been closed. Please reopen the connection before sending commands.")
        else:
            #TODO what to do when no errors are being thrown around
            pass
    
    def print(self, text) -> None:
        """
        Print information
    
        """

        if self._verbose:
            print(text)

    def open(self, device_identifier : str):
        """
        Open a connection to the card and return the handle
    
        Parameters
        ----------
        self._handle
            the handle object used for the card connection
        self._closed
            the indicator that indicated whether a connection is opened or closed is set to open (False)
        """

        self._handle = pyspcm.spcm_hOpen(pyspcm.create_string_buffer(bytes(device_identifier, 'utf-8')))
        self._closed = False
    
    @staticmethod
    def close(handle : pyspcm.drv_handle) -> None:
        """
        Close a connection to the card using a handle
    
        Parameters
        ----------
        handle
            the handle object used for the card connection that is closed
        """

        pyspcm.spcm_vClose(handle)

class Card(Device):
    """a class to control Spectrum Instrumentation cards

    For more information about what setups are available, please have a look at the user manual
    for your specific card.

    Parameters
    ----------
    buffer
        numpy object that can be used to write data into the spcm buffer

    Methods
    ----------
    product_name(self) -> str
        returns the product name of the active card, e.g. 'M4i.6621-x8'
    
    sn(self)
        returns the serial number of the active card
    
    sample_rate(self, sample_rate : int = None) -> (int)
        sets or gets the current sample rate of the handled card
    
    out_enable(self, channel_index : int, enable : bool)
        enables or disables the hardware output channel 'channel_index' of the active card

    out_amp(self, channel_index : int, value : int)
        sets the output range (amplitude) of the hardware channel 'channel_index' to [-value, +value] mV

    allocate_buffer(self, buffer_size : int)
        allocates a numpy object and connects it to the spcm buffer on the card
    
    start_buffer_transfer(self, *args):
        Start the transfer of the data to the card using the M2CMD_DATA_STARTDMA command

    Exceptions
    ----------
    SpcmException : (interface) class
        the main class to control exceptions that are raised due to errors that are raised 
        by the low-level driver. This exception is raised by the internal function 
        _check_error if the internal parameter _throw_error is True. All the get and set
        methods use the _check_error function to check for errors.
    """
    # public
    buffer = None  # External numpy buffer object
    buffer_size = 0

    # private
    _buffer = None # Internal numpy ctypes buffer object
    _buffer_alignment = 4096
    
    ## High-level parameter functions, that use the low-level get and set function
    def set_card_mode(self, card_mode : int) -> None:
        """
        Set the card mode
        
        Parameters
        ----------
        card_mode : int
            the mode that the card needs to operate in

        Raises
        ------
        SpcmException
        """
        
        self.set(SPC_CARDMODE, card_mode)

    def product_name(self) -> str:
        """
        Get the product name of the card (e.g. M4i.6622-x8)

        Raises
        ------
        SpcmException
    
        Returns
        -------
        str
        """

        return spcm_tools.szTypeToName(self.get(pyspcm.SPC_PCITYP))
    
    def sn(self) -> int:
        """
        Get the serial number of a product (e.g. 12345)

        Raises
        ------
        SpcmException
    
        Returns
        -------
        int
        """

        return self.get(SPC_PCISERIALNO)
    
    def sample_rate(self, sample_rate : int = None) -> int:
        """Sets or gets the current sample rate of the handled card

        Parameters
        ----------
        sample_rate : int = None
            if the parameter sample_rate is given with the function call, then the card's sample rate is set to that value
            if the parameter sample_rate is not give, the method returns the actual sample rate"""
        
        if sample_rate is not None:
            self.set(SPC_SAMPLERATE, sample_rate)
            return None
        else:
            return self.get(SPC_SAMPLERATE)
    
    def out_enable(self, channel_index : int, enable : bool) -> None:
        """
        Enables an output channel of the card

        Raises
        ------
        SpcmException
    
        Parameters
        ----------
        channel_index : int
            The index of the channel to be enabled.
        enable : bool
            Turn-on (True) or off (False) the spezific channel
        """

        self.set(SPC_ENABLEOUT0 + (SPC_ENABLEOUT1 - SPC_ENABLEOUT0) * channel_index, int(enable))
        
    def out_amp(self, channel_index : int, value : int) -> None:
        """
        Sets the output range (amplitude) of the card in mV

        Raises
        ------
        SpcmException
    
        Parameters
        ----------
        channel_index : int
            The index of the channel to be enabled.
        value : int
            The output range (amplitude) of the specific channel in millivolts
        """

        self.set(SPC_AMP0 + (SPC_AMP1 - SPC_AMP0) * channel_index, value)

    def allocate_buffer(self, buffer_size : int = None, num_samples : int = None, sample_type = np.int16) -> None:
        """Memory allocation for the buffer that is used for communicating with the card

        Parameters
        ----------
        buffer_size : int = None
            the size of the allocated buffer in Bytes
        num_samples : int = None
            in stead of allocated buffer size directly, use the number of samples an get the number of active channels and bytes per samples directly from the card
        sample_type = np.int16
            the type of element used in the numpy array
        """

        if buffer_size:
            self.buffer_size = buffer_size
        elif num_samples:
            num_channels = self.get(SPC_CHCOUNT)
            bytes_per_sample = self.get(SPC_MIINST_BYTESPERSAMPLE)
            self.buffer_size = num_samples * bytes_per_sample * num_channels
        else:
            raise SpcmException(text="Buffer allocation: either give a buffer size or a number of samples")
        dwMask = self._buffer_alignment - 1

        item_size = sample_type(0).itemsize
        # allocate a buffer (numpy array) for DMA transfer: a little bigger one to have room for address alignment
        databuffer_unaligned = np.empty(((self._buffer_alignment + self.buffer_size) // item_size, ), dtype = sample_type)   # half byte count at int16 sample (// = integer division)
        # two numpy-arrays may share the same memory: skip the begin up to the alignment boundary (ArrayVariable[SKIP_VALUE:])
        # Address of data-memory from numpy-array: ArrayVariable.__array_interface__['data'][0]
        start_pos_samples = ((self._buffer_alignment - (databuffer_unaligned.__array_interface__['data'][0] & dwMask)) // item_size)
        self.buffer = databuffer_unaligned[start_pos_samples:start_pos_samples + (self.buffer_size // item_size)]   # byte address but int16 sample: therefore / 2
        if num_channels and num_samples:
            self.buffer = self.buffer.reshape((num_channels, num_samples), order='F')
        self._buffer = self.buffer.ctypes.data_as(pyspcm.c_void_p)
    
    def start_buffer_transfer(self, *args, buffer_type=SPCM_BUF_DATA, direction=SPCM_DIR_PCTOCARD, notify_size=0, transfer_offset=0, transfer_length=None):
        """Start the transfer of the data to the card using the M2CMD_DATA_STARTDMA command
        
        Parameters
        ----------
        *args : list
            list of additonal arguments that are added as flags to the start dma command
        """

        if transfer_length is None: transfer_length = self.buffer_size
        
        # we define the buffer for transfer and start the DMA transfer
        self.print("Starting the DMA transfer and waiting until data is in board memory")
        pyspcm.spcm_dwDefTransfer_i64(self._handle, buffer_type, direction, notify_size, self._buffer, transfer_offset, transfer_length)
        cmd = M2CMD_DATA_STARTDMA
        for arg in args:
            cmd |= arg
        self.cmd(cmd)
        self.print("... data has been transferred to board memory")
