import board
import busio
import digitalio
import adafruit_max31855
import logging


class MAX31855:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs = digitalio.DigitalInOut(board.D5)

        self.last_t = 0
        self.sensor = adafruit_max31855.MAX31855(spi, cs)

    def get_temperature(self):
        try:
            temp = self.sensor.temperature
            self.last_t = temp
        except RuntimeError as ex:
            self.logger.error('Temp2 31855 crash: ' + str(ex))
            temp = self.last_t

        return temp
