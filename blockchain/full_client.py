import logging

import random
import requests
from orderedset import OrderedSet
from .block import Block
from .chain import Chain
from .config import CONFIG
from .transaction import *


class FullClient(object):
    """docstring for FullClient"""
    def __init__(self):
        # Mock nodes by hard coding
        self.nodes = ["http://127.0.0.1:9000"]
        self.public_key = "123"
        self.chain = Chain(self.public_key)
        # Transaction set needs to be implemented, right out it is just a set
        self.transaction_set = OrderedSet()
        self.invalid_transactions = set()

        self.recover_after_shutdown()

    def handle_new_transaction(self, transaction):
        transaction_object = eval(transaction)
        # We only want to broadcast a tx if it already is in the queue or in the chain
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
        new_block = Block(self.chain.last_block().get_block_information())

        for _ in range(CONFIG["block_size"]):
            # TODO: transaction validation
            # or do we want it before we add it to the transaction set
            if len(self.transaction_set):
                transaction = self.transaction_set.pop()
                if transaction:
                    new_block.add_transaction(transaction)
                else:
                    self.invalid_transactions.add(transaction)
            else:
                # Break if transaction set is empty
                break
        new_block.update_hash()
        return new_block

    def submit_block(self, block):
        # TODO: block validation
        if block:
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
