"""
Auhtor: vlad at smirnov.com
License: No license needed. Use it free whatever you like.
This implements support for ultrasonic distance sensor HC-SR04
"""

from nanpy import SerialManager
from nanpy.arduinoboard import ArduinoObject
from nanpy.arduinoboard import (arduinoobjectmethod, returns)

class MHZ19(ArduinoObject):
    firmware_id='MHZ19'

    def __init__(self, pwmPin, connection = None):
        ArduinoObject.__init__(self, connection = connection)
        self.id = self.call('new', pwmPin)

    @returns(int)
    @arduinoobjectmethod
    def read(self):
        """
        Returns distance from object (in millimiters).
        :return:
        """
        pass

if __name__ == "__main__":
    """
    A sample of the module use.
    Displays 100 readings with a 1 sec delay in between.
    """
    from time import sleep
    c = SerialManager()
    hc = MHZ19(11) #
    for i in range(100):
        print "%d. got response: %d" %(i+1,hc.read())
        sleep(3)



