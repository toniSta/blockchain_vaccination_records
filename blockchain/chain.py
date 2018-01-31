"""This module implements the chain functionality."""
import logging
import os
from collections import deque
from threading import RLock, current_thread
from .block import Block
from .config import CONFIG
from blockchain.transaction import *
from anytree import Node, RenderTree

logger = logging.getLogger("blockchain")


class Chain(object):
    """Basic chain class."""

    __instance = None

    def __new__(cls, load_persisted=True):
        """Create a singleton instance of the chain."""
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, load_persisted=True):
        """Create initial chain and tries to load saved state from disk."""
        self.chain = None
        self.genesis = None
        self.block_creation_cache = deque()
        self.vaccine_cache = set()
        self.doctors_cache = set()
        self._lock = RLock()
        if load_persisted and self._can_be_loaded_from_disk():
            self._load_from_disk()

    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()
        if exc_type or exc_val or exc_tb:
            logger.exception("Thread '{}' got an exception within a with \
                             statement. Type: {}; Value: {}; Traceback:"
                             .format(
                                 current_thread(),
                                 exc_type,
                                 exc_val))

    def __str__(self):
        return str(RenderTree(self.genesis))

    def _can_be_loaded_from_disk(self):
        """Return if the blockchain can be loaded from disk.

        True if the blockchain persistance folder
        and the genesis block file are present.
        """
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
        with self._lock:
            Node(block.hash, parent=block.previous_block, block=block)
            self._update_caches(block, self.block_creation_cache, self.doctors_cache, self.vaccine_cache)

    def _update_caches(self, block, block_creation_cache, doctors_cache, vaccine_cache):
        """Update the block creation cache and refresh the registered doctors and vaccines."""
        with self._lock:
            self._update_block_creation_cache(block, block_creation_cache)
            for transaction in block.transactions:
                if type(transaction).__name__ == "PermissionTransaction":
                    if transaction.requested_permission is Permission.doctor:
                        doctors_cache.add(transaction.sender_pubkey)
                elif type(transaction).__name__ == "VaccineTransaction":
                    vaccine_cache.add(transaction.vaccine)

    def _update_block_creation_cache(self, block, block_creation_cache):
        """Refresh the block creation cache.

        Moves the current block creator to the right side of the queue,
        adds any new admission nodes to the left side of the queue in the order
        they appear in the block.
        """
        with self._lock:
            block_creator = block.public_key
            if block_creator in block_creation_cache:
                block_creation_cache.remove(block_creator)
            block_creation_cache.append(block_creator)
            for transaction in block.transactions:
                if type(transaction).__name__ == "PermissionTransaction":
                    if transaction.requested_permission is Permission.admission:
                        block_creation_cache.appendleft(transaction.sender_pubkey)

    def find_block_by_hash(self, hash):
        """Find a block by its hash. Return None if hash not found."""
        block_node = find(self.genesis, lambda node: node.name == hash)
        if block:
            return block_node.block
        return

    def get_leaves(self):
        """Return the last block of the chain."""
        with self._lock:
            leaves = anytree.search.findall(self.genesis, lambda node: node.is_leaf == True)
            return [leaf.block for leaf in leaves]

    def side_chain(self, node_hash):
        """Delete a side chain by removing a branch.

        Remove a whole branch detaching its root node.
        """
        with self._lock:
            node_to_delete = anytree.search.find(self.genesis, lambda node: node.hash == node_hash)
            if node_to_delete:
                node_to_delete.parent = None
            else:
                logger.info("Block with hash {} not found".format(node_hash))

    def get_block_creation_history(self, n):
        """Return public keys of the oldest n blockcreating admission nodes. Return None if n is out of bounds."""
        with self._lock:
            if n > len(self.block_creation_cache) or n < 0:
                return
            block_creation_history = []
            for i in range(n):
                block_creation_history.append(self.block_creation_cache[i])
            return block_creation_history

    def get_admissions(self):
        """Return set of currently registered admissions."""
        with self._lock:
            return set(self.block_creation_cache)   # in case of changing this method do not return a reference to the original deque!

    def get_doctors(self):
        """Return set of currently registered doctors."""
        with self._lock:
            return set(self.doctors_cache)  # in case of changing this method do not return a reference to the original set!

    def get_vaccines(self):
        """Return set of currently registered vaccines."""
        with self._lock:
            return set(self.vaccine_cache)  # in case of changing this method do not return a reference to the original set!

    def get_registration_caches(self):
        """Return a tuple of sets containing the currently registered admissions, doctors, and vaccines."""
        with self._lock:
            return set(self.block_creation_cache), set(self.doctors_cache), set(self.vaccine_cache)

    def get_registration_caches_by_blockhash(self, hash):
        """Return a tuple of sets containing the registered admissions, doctors,
        and vaccines at the blockheight of the given hash."""
        with self._lock:
            block_creation_cache = deque()
            doctors_cache = set()
            vaccine_cache = set()
            max_chain_index = self.size() - 1
            current_index = 0
            while current_index <= max_chain_index:
                current_block = self.find_block_by_index(current_index)
                self._update_caches(current_block, block_creation_cache, doctors_cache, vaccine_cache)
                if current_block.hash == hash:
                    return set(block_creation_cache), set(doctors_cache), set(vaccine_cache)
                if current_index == max_chain_index:
                    return None  # given block hash was not in the chain
                current_index += 1

    def get_registration_caches_by_blockindex(self, index):
        """Return a tuple of sets containing the registered admissions, doctors,
        and vaccines at the blockheight of the given blockindex."""
        with self._lock:
            if (index < 0 or index > self.size() - 1):
                return None  # given index is out of bounds
            block_creation_cache = deque()
            doctors_cache = set()
            vaccine_cache = set()
            current_index = 0
            while current_index <= index:
                current_block = self.find_block_by_index(current_index)
                self._update_caches(current_block, block_creation_cache, doctors_cache, vaccine_cache)
                current_index += 1
            return set(block_creation_cache), set(doctors_cache), set(vaccine_cache)

    def lock_state(self):
        return self._lock._is_owned()
