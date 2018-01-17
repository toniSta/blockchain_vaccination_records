"""This module implements block functionality.

The block class provides necessary methods for block creation and
serialization. Furthermore, the creation of the genesis block is
implemented here.
Block validation is not and will not be implemented in here.
"""

import logging
import os
from hashlib import sha256
from time import time

from .config import CONFIG
from blockchain.transaction import *

# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format="[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("blockchain")


class Block(object):
    """This class represents a block in the blockchain."""

    def __init__(self, data, public_key=None):
        # data object can be:
        #   1. header information of the previous block
        #   2. string representation of a block
        if type(data) == dict:
            self._from_dictionary(data)
            assert public_key
            self.public_key = public_key
        elif type(data) == str:
            self._from_string(data)
        else:
            raise ValueError("Given argument is neither string nor dict!")

    def __repr__(self):
        """Create a string representation of the current block for hashing."""
        fields = [str(self.index), self.previous_block, self.version,
                  self.timestamp, self.public_key]
        if self.hash != "":
            fields.append(self.hash)
        block = CONFIG["serializaton"]["separator"].join(fields)
        block += CONFIG["serializaton"]["line_terminator"]
        for transaction in self.transactions:
            block += repr(transaction) + CONFIG["serializaton"]["line_terminator"]
        return block

    def __str__(self):
        return ("=======================\n"
                "  Block {}\n"
                "  Previous block: {}\n"
                "  Number of transactions: {}\n"
                "  hash: {}\n"
                "=======================").format(self.index,
                                                  self.previous_block,
                                                  len(self.transactions),
                                                  self.hash)

    def _from_string(self, data):
        """Recreate a block by its string representation.

        Recreate a block object based on a given string representation
        of a block. This will create a new object with the same attributes.
        """
        fields = ["index",
                  "previous_block",
                  "version",
                  "timestamp",
                  "public_key",
                  "hash"]
        header, transactions = data.split(
            CONFIG["serializaton"]["line_terminator"], 1)
        header_content = header.split(CONFIG["serializaton"]["separator"])
        header_information = dict(zip(fields, header_content))
        assert len(fields) == len(header_information), "Wrong header format!"
        self.index = int(header_information["index"])
        self.previous_block = header_information["previous_block"]
        self.version = header_information["version"]
        self.timestamp = header_information["timestamp"]
        self.public_key = header_information["public_key"]
        # Block ends with \n. Thus, splitting by line terminator will create
        # an empty string. We have to ignore this at this point.
        transaction_list = transactions.split(
            CONFIG["serializaton"]["line_terminator"])[:-1]
        self.transactions = [eval(tx) for tx in transaction_list]
        self.hash = header_information["hash"]

    def _from_dictionary(self, data):
        """Create a successor block based on header information."""
        logger.debug("Creating new block")
        self.index = int(data["index"]) + 1
        self.previous_block = data["hash"]
        self.version = CONFIG["version"]
        self.timestamp = str(int(time()))
        self.transactions = []
        self.hash = ""

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_block_information(self):
        """Return the necessary information for creating a new block."""
        return {
            "version": self.version,
            "index": self.index,
            "previous_block": self.previous_block,
            "timestamp": self.timestamp,
            "hash": self.hash
        }

    def persist(self):
        """Write the block into a file for persistency."""
        persistence_folder = CONFIG["persistance_folder"]
        os.makedirs(persistence_folder, exist_ok=True)
        file_path = os.path.join(persistence_folder, str(self.index))
        with open(file_path, "w") as block_file:
            block_file.write(repr(self))
        logging.debug("Block {} written to disk.".format(self.index))

    def update_hash(self):
        """Add hash to the final state of the block."""
        sha = sha256()
        sha.update(repr(self).encode("utf-8"))
        self.hash = sha.hexdigest()
        logger.debug("Finished creation of block:\n{}".format(str(self)))


def create_initial_block(public_key):
    """Create the genesis block."""
    logger.info("Creating new genesis block")
    genesis = Block({
        "index": -1,
        "hash": str(0)
    }, public_key)
    genesis.update_hash()
    return genesis
