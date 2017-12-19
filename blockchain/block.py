import logging
from hashlib import sha256
from time import time

from .config import CONFIG

# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format='[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger('blockchain')


class Block(object):
    def __init__(self, dictionary):
        logger.debug('Creating new block')
        self.version = CONFIG['version']
        self.previous_block = dictionary['hash']
        self.merkle = dictionary['merkle']
        self.timestamp = int(time())
        self.index = dictionary['index'] + 1
        self.transactions = []
        self.hash = ''

    def __str__(self):
        return ('=======================\n'
                '  Block {}\n'
                '  Previous block: {}\n'
                '  Merkle root: {}\n'
                '  Number of transactions: {}\n'
                '  hash: {}\n'
                '=======================').format(self.index,
                                                  self.previous_block,
                                                  self.merkle,
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

    # Add hash to the final state of the block
    def update_hash(self):
        sha = sha256()
        sha.update(str(self._get_relevant_data_for_hashing()).encode('utf-8'))
        self.hash = sha.hexdigest()
        logger.debug('Finished creation of block:\n{}'.format(str(self)))


def create_initial_block():
    '''Creates the genesis block.'''
    logger.info('Creating new genesis block')
    return Block({
        'previous_block': 0,
        'merkle': 0,
        'index': -1,
        'hash': 0
    })
