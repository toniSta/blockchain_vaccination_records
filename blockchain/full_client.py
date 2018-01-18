import logging
import os

import random
import requests
import sched
import time
from threading import Thread
from orderedset import OrderedSet
from .block import Block
from .chain import Chain
from .config import CONFIG
from .transaction import *
from .helper.cryptography import generate_keypair
from Crypto.PublicKey import RSA

logger = logging.getLogger("client")
scheduler = sched.scheduler(time.time, time.sleep)


class FullClient(object):
    """docstring for FullClient"""
    def __init__(self):
        # Mock nodes by hard coding
        self.nodes = ["http://127.0.0.1:9000"]
        self._setup_public_key()

        self.chain = Chain(self.public_key)

        self.transaction_set = OrderedSet()
        self.invalid_transactions = set()

        self.recover_after_shutdown()
        self._start_runner()

    def _start_runner(self):
        """Spawn thread for block creation."""
        thread = Thread(target=self._schedule)
        thread.start()

    def _schedule(self):
        """Start scheduler."""
        scheduler.enter(CONFIG["block_time"], 1, self._create_block, (scheduler,))
        scheduler.run()

    def _create_block(self, sc):
        """Create block and schedule next event."""
        self.determine_block_creation_node()
        scheduler.enter(CONFIG["block_time"], 1, self._create_block, (sc,))

    def determine_block_creation_node(self):
        # TODO: implement node selection algorithm
        new_block = self.create_next_block()
        self.submit_block(new_block)

    def _setup_public_key(self):
        """Create new key pair if necessary.

        Create a public/private key pair on setup and save them in files. If
        the full client restarts, file will be read in.
        """
        key_folder = CONFIG["key_folder"]
        if not os.path.isdir(key_folder) or os.listdir(key_folder) == []:
            # No keys present, so generate new pair
            os.makedirs(CONFIG["key_folder"], exist_ok=True)

            logger.info("Generating new public/private key pair")
            self.public_key, self.private_key = generate_keypair()

            path = os.path.join(key_folder, CONFIG["key_file_names"][0])
            with open(path, "wb") as key_file:
                key_file.write(self.public_key.exportKey())

            path = os.path.join(key_folder, CONFIG["key_file_names"][1])
            with open(path, "wb") as key_file:
                key_file.write(self.private_key.exportKey())

        elif set(os.listdir(key_folder)) != set(CONFIG["key_file_names"]):
            # One key is missing
            logger.error("Public or Private key are not existent!")
            assert os.listdir(key_folder) == CONFIG["key_file_names"]

        else:
            # Keys are present
            path = os.path.join(key_folder, CONFIG["key_file_names"][0])
            with open(path, "rb") as key_file:
                self.public_key = RSA.import_key(key_file.read())

            path = os.path.join(key_folder, CONFIG["key_file_names"][1])
            with open(path, "rb") as key_file:
                self.private_key = RSA.import_key(key_file.read())

    def handle_new_transaction(self, transaction):
        transaction_object = eval(transaction)
        # We only want to broadcast a tx if it is neither in the queue nor in the chain
        try:
            self.transaction_set.index(transaction_object)
        except ValueError:
            self.transaction_set.add(transaction_object)
            # TODO: check if it is in the chain already
            self._broadcast_new_transaction(transaction)

    def synchronize_blockchain(self):
        random_node = random.choice(self.nodes)
        last_block_remote = self._get_status_from_different_node(random_node)
        if last_block_remote.index == self.chain.last_block().index and \
           last_block_remote.hash == self.chain.last_block().hash:
            # blockchain is up-to-date
            return
        # TODO: implement synchronization
        if last_block_remote.index == self.chain.last_block().index and \
           last_block_remote.hash != self.chain.last_block().hash:
            # TODO: at least last block is wrong
            pass

        if last_block_remote.index != self.chain.last_block().index:
            # TODO: chain is outdated
            pass

    def create_next_block(self):
        new_block = Block(self.chain.last_block().get_block_information(),
                          self.public_key)

        for _ in range(CONFIG["block_size"]):
            if len(self.transaction_set):
                transaction = self.transaction_set.pop()
                if transaction.validate():
                    new_block.add_transaction(transaction)
                else:
                    self.invalid_transactions.add(transaction)
            else:
                # Break if transaction set is empty
                break
        new_block.update_hash()
        return new_block

    def submit_block(self, block):
        if block.validate():
            self.chain.add_block(block)
            # self._broadcast_new_block()
            block.persist()
        else:
            # TODO: define behaviour
            pass

    def received_new_block(self, block_representation):
        logger.debug("Received new block: {}".format(repr(block_representation)))
        new_block = Block(block_representation)
        if new_block.validate():
            self.chain.add_block(block)
            self._broadcast_new_block(block)
            block.persist()

    def _broadcast_new_block(self, block):
        for node in self.nodes:
            route = node + "/new_block"
            requests.post(route, data=repr(block))

    def _broadcast_new_transaction(self, transaction):
        for node in self.nodes:
            route = node + "/new_transaction"
            requests.post(route, data=repr(transaction))

    def _get_status_from_different_node(self, node):
        random_node = random.choice(self.nodes)
        route = random_node + "/latest_block"
        block = requests.get(route)
        return Block(block.text)

    def recover_after_shutdown(self):
        # Steps:
        #   1. read in files from disk -> maybe in __init__ of chain
        #   2. sync with other node(s)
        pass
