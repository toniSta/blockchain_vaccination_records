"""This class represents a block in the blockchain."""

import logging
import os
from hashlib import sha256
from time import time

from .config import CONFIG

# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format='[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger('blockchain')


class Block(object):
    def __init__(self, previous_block):
        logger.debug('Creating new block')
        self.index = previous_block['index'] + 1
        self.previous_block = previous_block['hash']
        self.merkle_root = previous_block['merkle_root']
        self.version = CONFIG['version']
        self.timestamp = str(int(time()))
        self.transactions = []
        self.hash = ''

    def __repr__(self):
        """Create a string representation of the current block for hashing."""
        fields = [str(self.index), self.previous_block, self.merkle_root,
                  self.version, self.timestamp]
        if self.hash != '':
            fields.append(self.hash)
        header = CONFIG['serializaton']['separator'].join(fields)
        header += CONFIG['serializaton']['line_terminator']
        block = header
        for transaction in self.transactions:
            block += transaction + CONFIG['serializaton']['line_terminator']
        return block

    def __str__(self):
        return ('=======================\n'
                '  Block {}\n'
                '  Previous block: {}\n'
                '  Merkle root: {}\n'
                '  Number of transactions: {}\n'
                '  hash: {}\n'
                '=======================').format(self.index,
                                                  self.previous_block,
                                                  self.merkle_root,
                                                  len(self.transactions),
                                                  self.hash)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_block_information(self):
        '''Returns the necessary information for creating a new block.'''
        return {
            'version': self.version,
            'index': self.index,
            'previous_block': self.previous_block,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'hash': self.hash
        }

    def persist(self):
        """Write the block into a file for persistency."""
        blockchain_folder = 'blockchain'
        persistence_folder = os.path.join(blockchain_folder,
                                          CONFIG['persistance_folder'])
        os.makedirs(persistence_folder, exist_ok=True)
        file_path = os.path.join(persistence_folder, str(self.index))
        with open(file_path, 'w') as block_file:
            block_file.write(repr(self))
        logging.debug('Block {} written to disk.'.format(self.index))

    def update_hash(self):
        """Add hash to the final state of the block."""
        sha = sha256()
        sha.update(repr(self).encode('utf-8'))
        self.hash = sha.hexdigest()
        logger.debug('Finished creation of block:\n{}'.format(str(self)))


def deserialize(self):
    pass


def create_initial_block():
    """Create the genesis block."""
    logger.info('Creating new genesis block')
    merkle_root = sha256()
    # We hash the first index to get a constant merkle root
    merkle_root.update(str(0).encode('utf-8'))
    return Block({
        'merkle_root': merkle_root.hexdigest(),
        'index': -1,
        'hash': str(0)
    })
