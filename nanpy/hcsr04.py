"""
Auhtor: vlad at smirnov.com
License: No license needed. Use it free whatever you like.
This implements support for ultrasonic distance sensor HC-SR04
"""

from nanpy import SerialManager
from nanpy.arduinoboard import ArduinoObject
from nanpy.arduinoboard import (arduinoobjectmethod, returns)

class HCSR04(ArduinoObject):

    def __init__(self, trigPin, echoPin, connection = None):
        """
        Class constructor.
        :param trigPin: trigger Pin
        :param echoPin: eccho Pin
        :param connection: optional connection parameter. If not provided will attempt to connect to default usb port.
        (i think).
        """
        ArduinoObject.__init__(self, connection = connection)
        self.id = self.call('new', trigPin, echoPin)

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
    hc = HCSR04(2, 3, c) # 2, 3 are trigger and echo PINs respectively
    for i in range(100):
        print "%d. got response: %d" %(i+1,hc.read())
        sleep(1)



