import RPi.GPIO as GPIO
import spidev
import time
import datetime
import sys
import logging

#ANGLEPIN : A0
ANGLEPIN = 0

#LED : GPIO19
LEDPIN = 19

#datetime instance
dt_now = datetime.datetime.now()

#Logger settings
logger = logging.getLogger(__name__)
logger.setLevel(10) #logging outputs log of level Warning or higher by default...
date = dt_now.strftime('%Y-%m-%d %H:%M')
sh = logging.StreamHandler()
fh = logging.FileHandler(date + '.log')
logger.addHandler(sh)
logger.addHandler(fh)


#Log formatting
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
#log test
logger.info('#######LOGGER TEST#######')

#GPIO port settings
GPIO.setwarnings(False)
GPIO.setmode( GPIO.BCM)
GPIO.setup( LEDPIN, GPIO.OUT)

LED = GPIO.PWM(LEDPIN, 100)

#initialize
LED.start(0)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 5000

def is_integer(n):
	try:
		float(n)
	except ValueError:
		return False
	else:
		return float(n).is_integer()

#args settings
args = sys.argv
logshows = 0
for i in range(1, len(args) ):
	if args[i] == '-l':
		logshows = 1
	elif args[i] == '-led':
		if len(args) > i+1:
			if is_integer(args[i+1]):
				LEDPIN = int(args[i+1])
				i+=1
	elif args[i] == '-angle':
		if len(args) > i+1:
			if is_integer(args[i+1]):
				ANGLEPIN = int(args[i+1])
				i+=1
	else:
		pass


def readadc(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

def arduino_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


if __name__ == '__main__':
	try:
		while True:
			data = readadc(ANGLEPIN)
			if logshows == 1:
				logger.debug("adc : {:8} ".format(data))
			value = arduino_map(data, 0, 1023, 0, 100)
			LED.ChangeDutyCycle(value)
			time.sleep( 0.01 )
	except KeyboardInterrupt:
		LED.stop()
		GPIO.cleanup()
		spi.close()
		sys.exit(0)
