import time
import board
import busio
import digitalio
import adafruit_max31856
import adafruit_max31855

print('MAX31865 and MAX31855 two thermocouples')

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs1 = digitalio.DigitalInOut(board.D5)
cs2 = digitalio.DigitalInOut(board.D18)

sensor1 = adafruit_max31856.MAX31856(spi, cs1)
sensor2 = adafruit_max31855.MAX31855(spi, cs2)


while True:
	temp1 = sensor1.temperature
	temp2 = sensor2.temperature

	for k, v in sensor1.fault.items():
		if v:
			print('Sensor1 fault: ' + str(v))
	for k, v in sensor2.fault.items():
		if v:
			print('Sensor2 fault: ' + str(v))

	print('Temperature: {0:0.3f}C'.format(temp1))
	print('Temperature: {0:0.3f}C'.format(temp2))

	time.sleep(0.1)
