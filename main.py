"""This file is for playing around. Feel free to alter it."""

from blockchain.block import *

if __name__ == "__main__":
    genesis = create_initial_block()
    genesis.add_transaction("tx1")
    genesis.add_transaction("tx2")
    genesis.update_hash()
    # print(repr(asd))
    genesis.persist()

    blockstring = """0,0,5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9,0.0.1,1514293020,75b7361ae525937dac17337af4d1d82aee8bd5019c179b9e86750b7bc63f57ee
tx1
tx2"""

    deserialize(blockstring)
