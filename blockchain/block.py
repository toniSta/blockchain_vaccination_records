from hashlib import sha256
from time import time

from .config import CONFIG


class Block(object):
    def __init__(self, dictionary):
        self.version = CONFIG['version']
        self.previous_block = dictionary['hash']
        self.merkle = dictionary['merkle']
        self.timestamp = int(time())
        self.index = dictionary['index'] + 1
        self.transactions = []
        self.hash = ''

    def __str__(self):
        return ('=======================\n'
                '  Block {},\n'
                '  Previous block: {},\n'
                '  Number of transactions: {}\n'
                '  hash: {}\n'
                '=======================').format(self.index,
                                                  self.previous_block,
                                                  len(self.transactions),
                                                  self.hash)

    def _get_relevant_data_for_hashing(self):
        return {
            'version': self.version,
            'index': self.index,
            'previous_block': self.previous_block,
            'timestamp': self.timestamp,
            'merkle': self.merkle,
            'transactions': [tx for tx in self.transactions]
        }

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_block_information(self):
        '''Returns the necessary information for creating a new block.'''
        return {
            'version': self.version,
            'index': self.index,
            'previous_block': self.previous_block,
            'timestamp': self.timestamp,
            'merkle': self.merkle,
            'hash': self.hash
        }

    def update_hash(self):
        sha = sha256()
        sha.update(str(self._get_relevant_data_for_hashing()).encode('utf-8'))
        self.hash = sha.hexdigest()


def create_initial_block():
    return Block({
        'previous_block': 0,
        'merkle': 0,
        'index': -1,
        'hash': 0
    })
