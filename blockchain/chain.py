"""This module implements the chain functionality."""
import logging
import os
from collections import deque
from .block import *
from .config import CONFIG
from blockchain.transaction import *

logger = logging.getLogger("blockchain")


class Chain(object):
    """Basic chain class."""

    __instance = None

    def __new__(cls, pub_key, priv_key, load_persisted=True):
        """Create a singleton instance of the chain."""
        if not Chain.__instance:
            logger.info("Creating initial chain")
            Chain.__instance = object.__new__(cls)
        return Chain.__instance

    def __init__(self, pub_key, priv_key, load_persisted=True):
        """Create initial chain with genesis block."""
        self.chain = []
        self.block_creation_cache = deque()
        if load_persisted and self._can_be_loaded_from_disk():
            self._load_from_disk()
        else:
            self.add_block(create_initial_block(pub_key, priv_key))

    def _can_be_loaded_from_disk(self):
        """Returns if the blockchain can be loaded from disk.

        True if the blockchain persistance folder
        and the genesis block file are present."""
        return os.path.isdir(CONFIG["persistance_folder"]) and os.path.exists(
                os.path.join(CONFIG["persistance_folder"], "0"))

    def _load_from_disk(self):
        current_block = 0
        block_path = os.path.join(CONFIG["persistance_folder"], str(current_block))
        while os.path.exists(block_path):
            with open(block_path, "r") as block_file:
                logger.info("Loading block {} from disk".format(current_block))
                recreated_block = Block(block_file.read())
                self.add_block(recreated_block)
            current_block += 1
            block_path = os.path.join(CONFIG["persistance_folder"], str(current_block))
        logger.info("Finished loading chain from disk")

    def add_block(self, block):
        """Add a block to the blockchain."""
        self.chain.append(block)
        self._update_block_creation_cache(block)

    def _update_block_creation_cache(self, block):
        """Refreshes the block creation cache.

        Moves the current block creator to the right side of the queue,
        adds any new admission nodes to the left side of the queue in the order
        they appear in the block."""
        block_creator = bytes.fromhex(block.public_key)
        if block_creator in self.block_creation_cache:
            self.block_creation_cache.remove(block_creator)
        self.block_creation_cache.append(block_creator)
        for transaction in block.transactions:
            if type(transaction).__name__ == "PermissionTransaction":
                if transaction.requested_permission is Permission.admission:
                    self.block_creation_cache.appendleft(transaction.sender_pubkey)

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

    def get_oldest_blockcreator(self, n=0):
        """Return the public key of the nth oldest blockcreating admission node. Return None if n is out of bounds."""
        if n > len(self.block_creation_cache) or n < 0:
            return
        return self.block_creation_cache[n]

    def get_admissions(self):
        return set(self.block_creation_cache)   # in case of changing this method do not return a reference to the original deque!

    def size(self):
        """Get length of the chain."""
        return len(self.chain)
