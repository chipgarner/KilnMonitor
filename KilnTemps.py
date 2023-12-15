import Publish.publisher
import time
from Secrets import TEST_SECRET
import logging
import MAX31855
import MAX31856
import MCP9600

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logging.info('Get the temperatures, MAX31865 and MAX31855 two thermocouples')


class KilnTemps:
    def __init__(self, sensors):
        self.sensors = sensors
        self.pub = Publish.publisher.Publisher(TEST_SECRET)

    def publish_results(self, message):
        time_in_seconds = round(time.time() * 1000)
        time_stamped_message = {"ts": time_in_seconds, "values": message}
        self.pub.send_message(str(time_stamped_message))

    def loop(self):
        while True:
            for name, sensor in self.sensors.items():
                temp = sensor.get_temperature()
                message = {name, temp}
                self.publish_results(message)
                logging.info(name + ': {0:0.3f}C'.format(temp))

            time.sleep(5)


if __name__ == '__main__':
    sensors = {'Top 55': MAX31855.MAX31855(), 'Bottom 56': MAX31856.MAX31856()}
    sensors = {'Top 9600': MCP9600.MCP9600(), 'Bottom 56B': MAX31856.MAX31856()}

    kiln_temps = KilnTemps(sensors)
    kiln_temps.loop()
