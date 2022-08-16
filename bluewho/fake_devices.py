##
#     Project: BlueWho
# Description: Information and notification of new discovered bluetooth devices
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import random

from bluewho.constants import FILE_FAKE_DEVICES
from bluewho.functions import readlines
from bluewho.models.device_info import DeviceInfo


class FakeDevices(object):
    def __init__(self):
        """Fake devices' producer by reading the FILE_FAKE_DEVICES file"""
        self.devices = []
        for line in readlines(FILE_FAKE_DEVICES):
            # Skip comments
            if '#' in line:
                line = line.split('#', 1)[0]
            if line:
                name, address, class_type = line.split(' | ', 2)
                # Generate random MAC address
                if address == '<RANDOM>':
                    address = ':'.join(map(lambda number: f'{number:02x}',
                                           (random.randint(0, 255)
                                            for _ in range(6)))).upper()
                class_type = int(class_type,
                                 class_type.startswith('0x') and 16 or 10)
                device = DeviceInfo(address=address,
                                    name=name,
                                    device_class=class_type,
                                    last_seen=None,
                                    notify=True)
                self.devices.append(device)

    def fetch_one(self):
        """Fetch a single fake device"""
        return self.devices[random.randint(0, len(self.devices) - 1)]

    def fetch_max(self, count):
        """Fetch max count fake devices"""
        return random.sample(self.devices,
                             random.randint(1,
                                            count if count <= len(self.devices)
                                            else len(self.devices)))

    def fetch_many(self):
        """Fetch a random number of fake devices"""
        return random.sample(self.devices, random.randint(0,
                                                          len(self.devices)))

    def fetch_all(self):
        """Fetch all the fake devices"""
        return self.devices
