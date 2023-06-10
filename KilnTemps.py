import Publish.publisher
import time
from Secrets import TEST_SECRET
import logging
import board
import busio
import digitalio
import ada_max31856_modified
import adafruit_max31855

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logging.info('Get the temperatures, MAX31865 and MAX31855 two thermocouples')

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs1 = digitalio.DigitalInOut(board.D5)
cs2 = digitalio.DigitalInOut(board.D6)

sensor1 = ada_max31856_modified.MAX31856(spi, cs1)
sensor2 = adafruit_max31855.MAX31855(spi, cs2)
sensor1.averaging = 16


def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


publish_me = True


if publish_me:
    pub = Publish.publisher.Publisher(TEST_SECRET)


    def publish_results(temp, t2):
        message = {'T1 56': c_to_f(temp), 'T2 55': c_to_f(t2)}
        time_in_seconds = round(time.time() * 1000)
        time_stamped_message = {"ts": time_in_seconds, "values": message}
        pub.send_message(str(time_stamped_message))
else:
    def publish_results(temp, t2):
        pass


last_t2 = 0  # Save this and re-use on errors
t2_cold_junction = None

while True:
    temp1 = sensor1.temperature
    temp1_cj = sensor1.reference_temperature

    try:
        temp2 = sensor2.temperature
        last_t2 = temp2
        t2_cold_junction = sensor2.reference_temperature
    except RuntimeError as ex:
        logging.error('Temp2 31855 crash: ' + str(ex))
        temp2 = last_t2

    for k, v in sensor1.fault.items():
        if v:
            logging.error('Temp1 31856 fault: ' + str(k))

    logging.info('T1 56: {0:0.3f}F'.format(c_to_f(temp1)))
    logging.info('T1 cold junction: {0:0.3f}F'.format(c_to_f(temp1_cj)))
    logging.info('T2 55: {0:0.3f}F'.format(c_to_f(temp2)))
    logging.info('T2 cold junction: {0:0.3f}F'.format(c_to_f(t2_cold_junction)))
    logging.info('  ')

    publish_results(temp1, temp2)

    time.sleep(5)
