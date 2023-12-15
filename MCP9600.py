import board
import busio
import adafruit_mcp9600
import time
import logging

class MCP9600:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.mcp = adafruit_mcp9600.MCP9600(i2c)
        self.last_t = 0

    def get_temperature(self):
        try:
            temp = self.mcp.temperature
            self.last_t = temp
        except RuntimeError as ex:
            self.logger.error('MCP9600 error ' + str(ex))
            temp = self.last_t

        return self.mcp.temperature


