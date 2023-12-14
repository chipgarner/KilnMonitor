import board
import busio
import digitalio
import adafruit_max31856
import time
import logging


class MAX31856:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

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
                self.logger.error('Temp1 31856 fault: ' + str(k))

        return temp
