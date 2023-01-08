import logging
import board
import busio
import digitalio
import adafruit_max31856
import adafruit_max31855


class TempSensor:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
        logging.info('Get the temperatures, MAX31865 and MAX31855 two thermocouples')

        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs1 = digitalio.DigitalInOut(board.D5)
        cs2 = digitalio.DigitalInOut(board.D6)

        self.sensor1 = adafruit_max31856.MAX31856(spi, cs1)
        self.sensor2 = adafruit_max31855.MAX31855(spi, cs2)

    @staticmethod
    def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0
