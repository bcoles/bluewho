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

import configparser
import logging

from bluewho.constants import FILE_DEVICES
from bluewho.models.device_info import DeviceInfo

POSITION_LEFT = 'left'
POSITION_TOP = 'top'
SIZE_WIDTH = 'width'
SIZE_HEIGHT = 'height'

DEFAULT_VALUES = {}

SECTION_NOTIFY = 'notify'
SECTION_SCAN = 'scan'
SECTION_STARTUP = 'startup'

PREFERENCES_NOTIFICATION = 'show notification'
DEFAULT_VALUES[PREFERENCES_NOTIFICATION] = (SECTION_NOTIFY, True)

PREFERENCES_PLAY_SOUND = 'play sound'
DEFAULT_VALUES[PREFERENCES_PLAY_SOUND] = (SECTION_NOTIFY, True)

PREFERENCES_SCAN_SPEED = 'scan speed'
DEFAULT_VALUES[PREFERENCES_SCAN_SPEED] = (SECTION_SCAN, 4)

PREFERENCES_SHOW_LOCAL = 'show local'
DEFAULT_VALUES[PREFERENCES_SHOW_LOCAL] = (SECTION_SCAN, True)

PREFERENCES_STARTUPSCAN = 'startup scan'
DEFAULT_VALUES[PREFERENCES_STARTUPSCAN] = (SECTION_STARTUP, False)


class Settings(object):
    def __init__(self, filename, case_sensitive):
        # Parse settings from the configuration file
        self.config = configparser.RawConfigParser()
        # Set case sensitiveness if requested
        if case_sensitive:
            self.config.optionxform = str
        # Determine which filename to use for settings
        self.filename = filename
        logging.debug(f'Loading settings from {self.filename}')
        self.config.read(self.filename)

    def get(self, section, option, default=None):
        """Get an option from a specific section"""
        if (self.config.has_section(section) and
                self.config.has_option(section, option)):
            return self.config.get(section, option)
        else:
            return default

    def set(self, section, option, value):
        """Save an option in a specific section"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def get_boolean(self, section, option, default=None):
        """Get a boolean option from a specific section"""
        return self.get(section, option, default) == '1'

    def set_boolean(self, section, option, value):
        """Save a boolean option in a specific section"""
        self.set(section, option, '1' if value else '0')

    def get_int(self, section, option, default=0):
        """Get an integer option from a specific section"""
        return int(self.get(section, option, default))

    def set_int(self, section, option, value):
        """Set an integer option from a specific section"""
        self.set(section, option, int(value))

    def get_list(self, section, option, separator=','):
        """Get an option list from a specific section"""
        value = self.get(section, option, '')
        if len(value):
            return [v.strip() for v in value.split(separator)]

    def load_preferences(self):
        """Load preferences"""
        for option in DEFAULT_VALUES:
            self.set_preference(option, self.get_preference(option))

    def get_preference(self, option):
        """Get a preference value by option name"""
        section, default = DEFAULT_VALUES[option]
        if isinstance(default, bool):
            method_get = self.get_boolean
        elif isinstance(default, int):
            method_get = self.get_int
        else:
            method_get = self.get
        return method_get(section=section,
                          option=option,
                          default=default)

    def set_preference(self, option, value):
        """Set a preference value by option name"""
        section, default = DEFAULT_VALUES[option]
        if isinstance(default, bool):
            method_set = self.set_boolean
        elif isinstance(default, int):
            method_set = self.set_int
        else:
            method_set = self.set
        return method_set(section=section,
                          option=option,
                          value=value)

    def save(self):
        """Save the whole configuration"""
        file_settings = open(self.filename, mode='w')
        logging.debug(f'Saving settings to {self.filename}')
        self.config.write(file_settings)
        file_settings.close()

    def get_sections(self):
        """Return the list of the sections"""
        return self.config.sections()

    def get_options(self, section):
        """Return the list of the options in a section"""
        return self.config.options(section)

    def unset_option(self, section, option):
        """Remove an option from a section"""
        return self.config.remove_option(section, option)

    def clear(self):
        """Remove every data in the settings"""
        for section in self.get_sections():
            self.config.remove_section(section)

    def restore_window_position(self, window, section):
        """Restore the saved window size and position"""
        if (self.get_int(section, SIZE_WIDTH) and
                self.get_int(section, SIZE_HEIGHT)):
            window.set_default_size(
                self.get_int(section, SIZE_WIDTH, -1),
                self.get_int(section, SIZE_HEIGHT, -1))
        if (self.get_int(section, POSITION_LEFT) and
                self.get_int(section, POSITION_TOP)):
            window.move(
                self.get_int(section, POSITION_LEFT),
                self.get_int(section, POSITION_TOP))

    def save_window_position(self, window, section):
        """Save the window size and position"""
        position = window.get_position()
        self.set_int(section, POSITION_LEFT, position[0])
        self.set_int(section, POSITION_TOP, position[1])
        size = window.get_size()
        self.set_int(section, SIZE_WIDTH, size[0])
        self.set_int(section, SIZE_HEIGHT, size[1])

    def load_devices(self):
        """Return the devices list from the configuration file"""
        devices = []
        if FILE_DEVICES.exists():
            logging.info('Loading the devices list')
            with open(FILE_DEVICES, 'r') as file:
                # Each device is separated by a single line with >
                lines = file.read().split('\n>\n')
                for line in lines:
                    if line:
                        line = line.split('\n')
                        device_class = int(line[2],
                                           16
                                           if line[2].startswith('0x')
                                           else 10)
                        device = DeviceInfo(address=line[0],
                                            name=line[1],
                                            device_class=device_class,
                                            last_seen=line[3],
                                            notify=False)
                        devices.append(device)
        return devices

    def save_devices(self, devices):
        """Save devices list to filename"""
        if len(devices) > 0:
            logging.info('Saving the devices list')
            with open(FILE_DEVICES, 'w') as file:
                for address in devices:
                    device = devices.get_iter(address)
                    file.write(f'{address}\n'
                               f'{devices.get_name(device)}\n'
                               f'{hex(devices.get_class(device))}\n'
                               f'{devices.get_last_seen(device)}\n'
                               '>\n')
        elif FILE_DEVICES.exists():
            logging.info('Deleting the devices list')
            FILE_DEVICES.unlink()
