# SPDX-FileCopyrightText: 2021 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using TCA9548A to perform a simple scan for connected devices
import board

import adafruit_tca9548a
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--address', type=hex, default=0x70, help='I2C address of the TCA9548A multiplexer')
arg_parser.add_argument('--channel', type=int, default=0, help='Channel to scan on the TCA9548A multiplexer')
args = arg_parser.parse_args()

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c, address=args.address)
print(len(tca))

for channel in range(8):
    if tca[channel].try_lock():
        print(f"Channel {channel}:", end="")
        addresses = tca[channel].scan()
        print([hex(address) for address in addresses if address != 0x70])
        tca[channel].unlock()
