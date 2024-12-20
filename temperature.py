# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.

import machine
import onewire
import ds18x20
import time
from .logger import Logger

class TemperatureSensor:
    _pin: int = 0
    _one_wire: onewire.OneWire
    _sensor: ds18x20.DS18X20
    _devices = []

    def __init__(self, pin: int) -> None:
        self._pin = pin
        self._one_wire = onewire.OneWire(machine.Pin(pin))  
        self._sensor = ds18x20.DS18X20(self._one_wire)
        self._devices = self._sensor.scan()
        Logger.print("Found devices:", self._devices)
        if not self._devices:
            raise RuntimeError("No DS18B20 found!")

    def get_temperature(self):
        for device in self._devices:
            self._sensor.convert_temp()
            time.sleep(1) 
            temp = self._sensor.read_temp(device)
            Logger.print("Temperature:", temp)
            return temp
        