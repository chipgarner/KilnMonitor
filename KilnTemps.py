import Publish.publisher
import time
from Secrets import TEST_SECRET
import logging
import MAX31855
import MAX31856

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logging.info('Get the temperatures, MAX31865 and MAX31855 two thermocouples')

sensor1 = MAX31856.MAX31856()
sensor2 = MAX31855.MAX31855()

publish_me = True

if publish_me:
    pub = Publish.publisher.Publisher(TEST_SECRET)


    def publish_results(temp, t2):
        message = {'T1 56': temp, 'T2 55': t2}
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


    logging.warning('T1 56: {0:0.3f}F'.format(temp1))
    logging.warning('T2 55: {0:0.3f}F'.format(temp2))
    logging.warning('  ')

    publish_results(temp1, temp2)

    time.sleep(5)


