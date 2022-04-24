# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
"""Sensor demo for Adafruit Feather Sense. Prints data from each of the sensors."""
import time
import array
import math
import board
import audiobusio
from machine import UART

uart = busio.UART(board.TX, board.RX, baudrate=9600)

microphone = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                              sample_rate=16000, bit_depth=16)

def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return int(math.sqrt(sum(float(sample - minbuf) *
                             (sample - minbuf) for sample in values) / len(values)))



while True:
    samples = array.array('H', [0] * 160)
    microphone.record(samples, len(samples))

    print("\nFeather Sense Sensor Demo")
    print("---------------------------------------------")
    soundLevel = normalized_rms(samples)
    
    print("Sound level:", soundLevel)
    if soundLevel > 100:
        print("Loud")
        msg = bytearray("loud\n\r".encode())
        print(msg)
        uart.write(msg)
        time.sleep(0.2)

    time.sleep(100)
