"""This module implements block functionality.

The block class provides necessary methods for block creation and
serialization. Furthermore, the creation of the genesis block is
implemented here.
Block validation is not and will not be implemented in here.
"""

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
    """This class represents a block in the blockchain."""

    def __init__(self, data):
        # data object can be:
        #   1. header information of the previous block
        #   2. string representation of a block
        if type(data) == dict:
            self._from_dictionary(data)
        elif type(data) == str:
            self._from_string(data)
        else:
            raise ValueError('Given argument is neither string nor dict!')

    def _from_string(self, data):
        """Recreate a block by its string representation.

        Recreate a block object based on a given string representation
        of a block. This will create a new object with the same attributes.
        """
        fields = ['index',
                  'previous_block',
                  'merkle_root',
                  'version',
                  'timestamp',
                  'hash']
        header, transactions = data.split(CONFIG['serializaton']['line_terminator'], 1)
        header_information = dict(zip(fields, header.split(CONFIG['serializaton']['separator'])))
        assert len(fields) == len(header_information), "Wrong header format!"
        self.index = header_information['index']
        self.previous_block = header_information['previous_block']
        self.merkle_root = header_information['merkle_root']
        self.version = header_information['version']
        self.timestamp = header_information['timestamp']
        # Block ends with \n. Thus, splitting by line terminator will create
        # an empty string. We have to ignore this at this point.
        self.transactions = transactions.split(
            CONFIG['serializaton']['line_terminator'])[:-1]

        self.hash = header_information['hash']

    def _from_dictionary(self, data):
        """Create a successor block based on header information."""
        logger.debug('Creating new block')
        self.index = data['index'] + 1
        self.previous_block = data['hash']
        self.merkle_root = data['merkle_root']
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
        block = CONFIG['serializaton']['separator'].join(fields)
        block += CONFIG['serializaton']['line_terminator']
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
        """Return the necessary information for creating a new block."""
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
