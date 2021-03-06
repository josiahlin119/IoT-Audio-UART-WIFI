# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# CircuitPython NeoPixel Color Picker Example
import time
import array
import math
import board
import audiobusio

import board
import neopixel

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
#instantiate microphone
microphone = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,sample_rate=16000, bit_depth=16)
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

#The function is used to normalize the sound data

def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return int(math.sqrt(sum(float(sample - minbuf) *(sample - minbuf) for sample in values) / len(values)))

while True:
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    ble.stop_advertising()
    samples = array.array('H', [0] * 160)
    microphone.record(samples, len(samples))
    print("\n Sound Level Sensor Demo")
    print("---------------------------------------------")
    print("Sound level:", normalized_rms(samples))
   
    while ble.connected:
        if normalized_rms(samples) > 600:
            result = 'Too Loud'
            print("The noise is too loud")
            uart.write(result.encode("utf-8"))
            data = uart.read(10) 
            time.sleep(0.2)
    time.sleep(0.1)
