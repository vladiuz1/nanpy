import fnmatch
import logging
import serial
import sys
import time
from serial.tools.list_ports import comports

DEFAULT_BAUDRATE = 115200

log = logging.getLogger(__name__)

PY3 = sys.version_info[0] == 3


class SerialManagerError(Exception):
    pass


def _auto_detect_serial_unix(preferred_list=None):
    import glob
    glist = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
    glist += ['/dev/ttyS0', '/dev/ttyS1']
    ret = []

    if preferred_list is None:
        preferred_list = ['*']
        
    for d in glist:
        for preferred in preferred_list:
            if fnmatch.fnmatch(d, preferred):
                ret.append(d)
    if len(ret) > 0:
        return ret

    for d in glist:
        ret.append(d)
    return ret


class NoneSerialManager(object):

    def write(self, val):
        pass

    def read(self):
        return ""

    def readline(self):
        return ""


class SerialManager(object):
    _serial = None

    def __init__(self, device=None,
                 baudrate=DEFAULT_BAUDRATE,
                 sleep_after_connect=2,
                 timeout=7,
                 rtscts=False):
        self.device = device
        self.baudrate = baudrate
        self.sleep_after_connect = sleep_after_connect
        self.timeout = timeout
        self.rtscts = rtscts

    def open(self, device=None):
        '''open connection'''
        if device:
            self.device = device

        if not self.device:
            ports = _auto_detect_serial_unix()
            if not len(ports):
                raise SerialManagerError("No port was set, and no port was found!")
            self.device = ports[0]
        log.debug('opening port:%s [%s baud]', self.device, self.baudrate)
        assert self.device
        self._serial = serial.Serial(self.device,
                                     self.baudrate,
                                     timeout=self.timeout,
                                     rtscts=self.rtscts)
        if self.sleep_after_connect:
            time.sleep(self.sleep_after_connect)
        self._serial.flushInput()

    def write(self, value):
        if not self._serial:
            self.open()
        log.debug('sending:%s', repr(value))
        if PY3:
            self._serial.write(bytes(value, 'latin-1'))
        else:
            self._serial.write(value)

    def readline(self):
        if not self._serial:
            self.open()
        s = self._serial.readline()
        log.debug('received:%s', repr(s))
        s = s.decode()
        if not len(s):
            raise SerialManagerError('Serial timeout!')
        return s

    def flush_input(self):
        '''Flush input buffer, discarding all it's contents.'''
        if not self._serial:
            self.open()
        self._serial.flushInput()

    def close(self):
        '''close connection'''
        if self._serial:
            self._serial.close()
            self._serial = None

def findSerialManagerByBoardID(board_id, baudrate=DEFAULT_BAUDRATE, sleep_after_connect=2, timeout=7, rtscts=False):
    """
    This function finds a connection by BOARD_ID set by "cfg.h" or Makefile. Very convenient if you have multiple
    arduino boards connected. But slow . It takes approximately the same variables as SerialManager.__init__:
    :param board_id: the board id as defined.
    :param baudrate:
    :param sleep_after_connect: Modify this to make it work faster. But at your risk.
    :param timeout:
    :param rtscts:
    :return: instance of SerialManager if successful otherwise None
    """
    from define import DefineFeature
    for p in comports():
        try:
            c = SerialManager( device= p[0], baudrate=baudrate, sleep_after_connect=sleep_after_connect, timeout=timeout, rtscts=rtscts)
            d = DefineFeature(connection=c)
            if board_id == d.get('BOARD_ID'):
                return c
        except:
            pass

serial_manager = SerialManager()

