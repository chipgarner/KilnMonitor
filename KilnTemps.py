import Publish.publisher
import time
from Secrets import TEST_SECRET
import logging
import board
import busio
import digitalio
import adafruit_max31856
import adafruit_max31855

logging.basicConfig(level=logging.INFO)
logging.info('Get the temperatures, MAX31865 and MAX31855 two thermocouples')

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs1 = digitalio.DigitalInOut(board.D5)
cs2 = digitalio.DigitalInOut(board.D6)

sensor1 = adafruit_max31856.MAX31856(spi, cs1)
sensor2 = adafruit_max31855.MAX31855(spi, cs2)


def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


pub = Publish.publisher.Publisher(TEST_SECRET)


def publish_results(temp, t2, t2_NIST):
    message = {'Kiln T1': c_to_f(temp), 'T2': c_to_f(t2), 'T2 NIST': c_to_f(t2_NIST)}
    time_in_seconds = round(time.time() * 1000)
    time_stamped_message = {"ts": time_in_seconds, "values": message}
    pub.send_message(str(time_stamped_message))


last_t2 = 0  # Save this and re-use on errors

while True:
    temp1 = sensor1.temperature

    try:
        temp2 = sensor2.temperature
        last_t2 = temp2
    except RuntimeError as ex:
        print('Temp2 31855 crash: ' + str(ex))
        temp2 = last_t2

    for k, v in sensor1.fault.items():
        if v:
            print('Temp1 sensor fault: ' + str(k))

    print('Temperature1: {0:0.3f}F'.format(c_to_f(temp1)))
    print('Temperature2: {0:0.3f}F'.format(c_to_f(temp2)))
    print('  ')

    publish_results(temp1, temp2)

    time.sleep(5)
