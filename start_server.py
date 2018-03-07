import logging

from blockchain.config import CONFIG
from blockchain.network.server import start_server
from blockchain.full_client import FullClient


def _set_logger_properties():
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.WARNING)
    urllib_logger = logging.getLogger("urllib3")
    urllib_logger.setLevel(logging.WARNING)


def _get_license_information():
    return """
    Store vaccination records on the blockchain.
    Copyright (C) 2018  Benedikt Bock, Alexander Preuß, Toni Stachewicz

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    \n\n"""


if __name__ == "__main__":
    print(_get_license_information())
    logging.basicConfig(level=CONFIG.loglevel,
                        format="[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    _set_logger_properties()
    full_client = FullClient()
    start_server(full_client)
