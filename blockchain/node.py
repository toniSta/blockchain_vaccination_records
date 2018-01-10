import logging

import random
from orderedset import OrderedSet
from .block import Block
from .chain import Chain
from .config import CONFIG


class Node(object):
    """docstring for Node"""
    def __init__(self):
        # Mock nodes by hard coding
        self.nodes = [1, 2, 3]
        self.chain = Chain()
        # Transaction set needs to be implemented, right out it is just a set
        self.transaction_set = OrderedSet()
        self.invalid_transactions = set()

        # self.synchronize_blockchain()

    def connect_to_nodes(self):
        """Connect to neighbour nodes in P2P network.

        This method will not be implemented, since we mock the network itself.
        """
        raise NotImplementedError

    def synchronize_blockchain(self):
        random_node = random.choice(self.nodes)
        last_block_remote = self._get_status_from_different_node(random_node)
        if self.chain.last_block() == last_block_remote:
            # blockchain is up-to-date
            return
        # TODO: implement synchronization
        if last_block_remote.index == self.chain.last_block().index and \
           last_block_remote.hash != self.chain.last_block().hash:
            # at least last block is wrong
            pass

        if last_block_remote.index == self.chain.last_block().index:
            # chain is outdated
            pass

    def create_next_block(self):
        new_block = Block(self.chain.last_block().get_block_information())

        for _ in range(CONFIG['block_size']):
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

    def _broadcast_block(self, block):
        for node in self.nodes:
            # TODO: implement block broadcast
            pass

    def submit_block(self, block):
        # TODO: block validation
        if block:
            self.chain.add_block(block)
            self._broadcast_block(block)
            block.persist()

    def _get_status_from_different_node(self, node):
        pass

    def recover_after_shutdown():
        pass
