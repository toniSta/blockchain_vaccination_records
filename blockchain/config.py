"""This module provides a collection of adjustable parameters."""

import logging
from abc import ABCMeta
import sys


class CONFIG(ABCMeta):
    """The CONFIG meta class holds the adjustable parameters."""

    # Log level of the whole system
    loglevel = logging.DEBUG
    # Current version
    version = "1.0.0"
    # Folder, where all blocks are written to disk
    persistance_folder = "blockchain/blockchain_files"
    # Serialization properties
    serializaton = {
        "separator": ",",
        "line_terminator": "\n"
    }
    # Maximum amount of transactions per block
    block_size = 1024
    # Create a block every n seconds. N has to be at least 2
    block_time = 15  # with 5 seconds you will get multiple locks per index due to network latency
    # Folder to store public/private key of the client
    key_folder = "blockchain/keys"
    # Names of key files
    key_file_names = ["public_key.bin", "private_key.bin"]
    # Network routes
    ROUTES = {
        "new_block": "/new_block",
        "block_by_hash": "/request_block/hash/<hash>",
        "new_transaction": "/new_transaction",
        "new_judgement": "/new_judgement",
        "sync_request": "/sync_request"
    }
    # Default port the flask server will run on
    default_port = 9000
    # Enable/disable extra sleep, when making network requests
    # in order to simulate network latency
    artificial_latency_enabled = False
    # Time interval the network component will wait before making a request
    # (values are seconds)
    sleep_interval = (0.1, 0.5)
