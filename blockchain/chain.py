import logging
from .block import create_initial_block


class Chain(object):
    __instance = None

    def __new__(cls):
        if not Chain.__instance:
            logging.info('Creating initial chain')
            Chain.__instance = object.__new__(cls)
        return Chain.__instance

    def __init__(self):
        self.chain = [create_initial_block()]

    def add_block(self, block):
        self.chain.append(block)

    def find_block_by_index(self, index):
        if index > self.size() - 1 or index < 0:
            return
        return self.chain[index]

    def find_block_by_hash(self, hash):
        chain_index = self.size() - 1
        while chain_index != 0:
            if self.chain[chain_index].hash == hash:
                return self.chain[chain_index]
            else:
                chain_index -= 1

    def last_block(self):
        return self.chain[-1]

    def size(self):
        return len(self.chain)
