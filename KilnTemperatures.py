#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Modified January 2023 by Chip Garner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
# import logging
# logging.basicConfig(level=logging.DEBUG)

import Publish.publisher
import time
from Secrets import TEST_SECRET

import board
import digitalio
import adafruit_max31856

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
cs.direction = digitalio.Direction.OUTPUT
thermocouple = adafruit_max31856.MAX31856(spi,cs)

# import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0

# Uncomment one of the blocks of code below to configure your Pi or BBB to use
# software or hardware SPI.

# Raspberry Pi software SPI configuration.
CLK = 25
CS = 24
DO = 18
sensor = MAX31855.MAX31855(CLK, CS, DO)

# Raspberry Pi hardware SPI configuration.
# SPI_PORT   = 0
# SPI_DEVICE = 0
# sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# BeagleBone Black software SPI configuration.
# CLK = 'P9_12'
# CS  = 'P9_15'
# DO  = 'P9_23'
# sensor = MAX31855.MAX31855(CLK, CS, DO)

# BeagleBone Black hardware SPI configuration.
# SPI_PORT   = 1
# SPI_DEVICE = 0
# sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

pub = Publish.publisher.Publisher(TEST_SECRET)

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
    temp = sensor.readTempC()
    internal = sensor.readInternalC()
    t2 = thermocouple.temperature
    print('           T2: {0:0.3F}*F'.format(c_to_f(t2)))
    print('           T1: {0:0.3F}*F'.format(c_to_f(temp)))
    print('T amp1: {0:0.3F}*F'.format(c_to_f(internal)))

    message = {'Kiln T1': c_to_f(temp), 'Amp T1': c_to_f(internal), 'T2': c_to_f(t2)}
    time_in_seconds = round(time.time() * 1000)
    time_stamped_message = {"ts": time_in_seconds, "values": message}
    pub.send_message(str(time_stamped_message))

    time.sleep(5)
