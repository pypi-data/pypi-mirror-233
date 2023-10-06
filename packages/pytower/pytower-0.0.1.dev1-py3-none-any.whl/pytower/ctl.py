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
import argparse
import os

from .core import deploy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--deploy', action='store_true', dest='deploy', help='Deploy')
    parser.add_argument('-r', '--redeploy', action='store_true', dest='redeploy', help='Redeploy')
    args = parser.parse_args()

    if args.deploy is True:
        deploy(ip=os.environ['IP'], domain_name=os.environ['DOMAIN_NAME'])
