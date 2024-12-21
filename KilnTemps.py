import Publish.publisher
import time
from Secrets import KILN
import logging
import MAX31855
import MAX31856
import MCP9600
import queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logging.info('Get the temperatures, MAX31865 and MAX31855 two thermocouples')


class KilnTemps:
    def __init__(self, sensors):
        self.sensors = sensors
        self.pub = Publish.publisher.Publisher(KILN)

        self.loop_time = 5
        for sensor in sensors:
            self.fifo = queue.Queue()
            six_minute_queue = 360 / self.loop_time # Not accurate

            now = round(time.time() - 10) # Don't divide by zero on the first loop
            for items in range(int(six_minute_queue)):
                self.fifo.put({'temp': 0, 'time': now})

    def publish_results(self, message):
        time_in_ms = round(time.time() * 1000)
        time_stamped_message = {"ts": time_in_ms, "values": message}
        self.pub.send_message(str(time_stamped_message))

    def loop(self):
        while True:
            message = {}
            for name, sensor in self.sensors.items():
                temp = sensor.get_temperature()
                message.update({name: temp})
                self.publish_results(message)
                logging.info(name + ': {0:0.3f}C'.format(temp))

                old_temp_time = self.fifo.get()
                now = round(time.time())
                temp_time = {'temp': temp, 'time': now}
                self.fifo.put(temp_time)
                delta_time = (now - old_temp_time['time']) / 3600.0
                delta_temp = temp - old_temp_time['temp']
                slope = delta_temp / delta_time
                logging.info(str(int(slope)) + 'C/hr')

            time.sleep(self.loop_time)


if __name__ == '__main__':
    sensors = {'Top 55 NIST': MAX31855.MAX31855(), 'Bottom 56B': MAX31856.MAX31856()}
#    sensors = {'Top 9600': MCP9600.MCP9600(), 'Bottom 56B': MAX31856.MAX31856()}

    kiln_temps = KilnTemps(sensors)
    kiln_temps.loop()
