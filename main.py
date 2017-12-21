"""This file is for playing around. Feel free to alter it."""

from blockchain.block import *

if __name__ == '__main__':
    genesis = create_initial_block()
    genesis.add_transaction('tx1')
    genesis.add_transaction('tx2')
    genesis.update_hash()
    # print(repr(asd))
    genesis.persist()
