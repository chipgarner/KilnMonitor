import Publish.publisher
import time
from Secrets import TEST_SECRET
import logging
import board
import busio
import digitalio
import adafruit_max31856
import adafruit_max31855

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logging.info('Get the temperatures, MAX31865 and MAX31855 two thermocouples')


class MAX31856:
    def __init__(self):
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs = digitalio.DigitalInOut(board.D6)

        sensor = adafruit_max31856.MAX31856(spi, cs)
        sensor.averaging = 16

        self.sensor = sensor

    def get_temperature(self):
        self.sensor.initiate_one_shot_measurement()
        time.sleep(1)
        temp = self.sensor.unpack_temperature()

        for k, v in self.sensor.fault.items():
            if v:
                logging.error('Temp1 31856 fault: ' + str(k))

        return temp


class MAX31855:
    def __init__(self):
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs = digitalio.DigitalInOut(board.D5)

        self.last_t = 0
        self.sensor = adafruit_max31855.MAX31855(spi, cs)

    def get_temperature(self):
        try:
            temp = self.sensor.temperature
            self.last_t = temp
        except RuntimeError as ex:
            logging.error('Temp2 31855 crash: ' + str(ex))
            temp = self.last_t

        return temp

# spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# cs2 = digitalio.DigitalInOut(board.D5)
#
sensor1 = MAX31856()
sensor2 = MAX31855()



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

print('Before while')
while True:
    print('While')
    temp1 = sensor1.get_temperature()
    temp2 = sensor2.get_temperature()


    logging.info('T1 56: {0:0.3f}F'.format(c_to_f(temp1)))
    logging.info('T2 55: {0:0.3f}F'.format(c_to_f(temp2)))
    logging.info('  ')

    publish_results(temp1, temp2)

    time.sleep(5)


