from Crypto.PublicKey import RSA
from blockchain.chain import Chain
from blockchain.block import Block
from blockchain.block import create_initial_block

import pytest
import os

PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())


def test_chain_is_singleton():
    chain_1 = Chain(load_persisted=False)
    chain_2 = Chain(load_persisted=False)
    assert id(chain_1) == id(chain_2)


@pytest.fixture()
def chain():
    chain = Chain(load_persisted=False)
    genesis = create_initial_block(PUBLIC_KEY, PRIVATE_KEY)
    chain.add_block(genesis)
    yield chain


@pytest.fixture()
def next_block(chain):
    block_information = chain.genesis_block.get_block_information()
    next_block = Block(block_information, PUBLIC_KEY)
    next_block.sign(PRIVATE_KEY)
    next_block.update_hash()
    yield next_block


def test_find_block_by_hash(chain, next_block):
    chain.add_block(next_block)
    hash = next_block.hash
    assert chain.find_block_by_hash(hash) == next_block
    assert chain.find_block_by_hash("some random hash") is None
