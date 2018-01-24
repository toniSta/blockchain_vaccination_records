import logging

from blockchain.config import CONFIG
from blockchain.network.server import start_server
from blockchain.full_client import FullClient


def _set_logger_properties():
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.WARNING)


if __name__ == "__main__":
    logging.basicConfig(level=CONFIG["loglevel"],
                        format="[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    _set_logger_properties()
    full_client = FullClient()
    start_server(full_client)
