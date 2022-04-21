# Write your code here :-)
# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
"""Sensor demo for Adafruit Feather Sense. Prints data from each of the sensors."""
import time
import array
import math
import board
import board
import busio
import audiobusio
uart = busio.UART(board.TX, board.RX, baudrate=9600)
i2c = board.I2C()
microphone = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                              sample_rate=16000, bit_depth=16)

def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return int(math.sqrt(sum(float(sample - minbuf) *
                             (sample - minbuf) for sample in values) / len(values)))

# apds9960.enable_proximity = True
# apds9960.enable_color = True

# Set this to sea level pressure in hectoPascals at your location for accurate altitude reading.
# bmp280.sea_level_pressure = 1013.25

while True:
    samples = array.array('H', [0] * 160)
    microphone.record(samples, len(samples))

    print("\n Sound Level Sensor Demo")

    print("---------------------------------------------")
    print("Sound level:", normalized_rms(samples))
    if normalized_rms(samples) > 600:
        print("The noise is too loud")
    
    data = uart.read(10) 
    time.sleep(0.2)

