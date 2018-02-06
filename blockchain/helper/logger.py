import logging
import os
from blockchain.config import CONFIG


def setup_basic_logger_config():
    logging.basicConfig(level=CONFIG["loglevel"])


def write_logs_to_file():
    logger = logging.getLogger("LogSetup")
    file_path = '/var/log/blockchain/server.log'
    logger.info("Set log output to file {}".format(file_path))
    os.makedirs(os.path.dirname(file_path))
    [logging.root.removeHandler(handler) for handler in logging.root.handlers[:]]
    logging.basicConfig(level=CONFIG["loglevel"], filename=file_path, filemode='a+')
