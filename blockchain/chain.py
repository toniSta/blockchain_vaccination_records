"""This module implements the chain functionality."""
import logging
from .block import create_initial_block


class Chain(object):
    """Basic chain class."""

    __instance = None

    def __new__(cls):
        """Create a singleton instance of the chain."""
        if not Chain.__instance:
            logging.info('Creating initial chain')
            Chain.__instance = object.__new__(cls)
        return Chain.__instance

    def __init__(self):
        """Create initial chain with genesis block."""
        self.chain = [create_initial_block()]

    def add_block(self, block):
        """Add a block to the blockchain."""
        self.chain.append(block)

    def find_block_by_index(self, index):
        """Find a block by its index. Return None at invalid index."""
        if index > self.size() - 1 or index < 0:
            return
        return self.chain[index]

    def find_block_by_hash(self, hash):
        """Find a block by its hash. Return None if hash not found."""
        chain_index = self.size() - 1
        while chain_index != 0:
            if self.chain[chain_index].hash == hash:
                return self.chain[chain_index]
            else:
                chain_index -= 1

    def last_block(self):
        """Return the last block of the chain."""
        return self.chain[-1]

    def size(self):
        """Get length of the chain."""
        return len(self.chain)
