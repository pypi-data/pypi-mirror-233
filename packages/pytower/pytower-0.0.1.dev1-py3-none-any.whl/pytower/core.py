"""
    pytower - Build and deploy Pythonic apps.
    Copyright (C) 2023  Salman Mohammadi <salman@pytower.com>

    This file is part of pytower.

    pytower free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pytower is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def deploy(ip, domain_name):
    """deploy the app"""
    txt = 'hello' + ' ' + ip + ' ' + domain_name
    print(txt)
