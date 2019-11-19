import spidev
import time
import sys
from sensor import *

if __name__ == '__main__':
    sensor = Sensor.generate(Sensors.LIGHT, 7)
    print(sensor.data)
    print(spi)
    try:
        while True: 
            print(sensor.read_data())
            print(sensor.PIN)
            print("{} : {:8} ".format(sensor.type,sensor.mapped_data()))
            time.sleep(0.5)
    except KeyboardInterrupt:
        del sensor
        sys.exit(0)
