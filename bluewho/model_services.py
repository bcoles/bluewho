##
#     Project: BlueWho
# Description: Information and notification of new discovered bluetooth devices.
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2021 Fabio Castelli
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

class ModelServices(object):
  COL_NAME = 0
  COL_PROTOCOL = 1
  COL_CHANNEL = 2
  def __init__(self, model):
    self.model = model

  def clear(self):
    "Clear the model"
    return self.model.clear()

  def add_service(self, service):
    "Add devices's services to the list"
    # Refer to bluetooth.find_service help section
    if service['name'] or service['protocol'] or service['port']:
      # Skipping services with no name, protocol and port
      return self.model.append((
        service['name'],
        service['protocol'],
        service['port']
      ))
