from blockchain.chain import Chain
from blockchain.block import Block

import pytest


def test_chain_is_singleton():
    chain_1 = Chain()
    chain_2 = Chain()
    assert id(chain_1) == id(chain_2)


@pytest.fixture()
def chain():
    chain = Chain()
    yield chain


def test_initial_chain_contains_genesis(chain):
    assert chain.size() == 1
    assert chain.find_block_by_index(0) == chain.last_block()


@pytest.fixture()
def chain_with_blocks(chain):
    next_block = Block(chain.find_block_by_index(0).get_block_information())
    next_block.update_hash()
    chain.add_block(next_block)
    successor = Block(next_block.get_block_information())
    successor.update_hash()
    chain.add_block(successor)
    yield chain


def test_find_block_by_hash(chain_with_blocks):
    index = 1
    block_to_find = chain_with_blocks.find_block_by_index(index)
    hash = chain_with_blocks.find_block_by_index(index).hash

    assert chain_with_blocks.find_block_by_hash(hash) == block_to_find


def test_find_with_wrong_parameters(chain_with_blocks):
    assert chain_with_blocks.find_block_by_hash("some random hash") is None
    assert chain_with_blocks.find_block_by_index(-1) is None
    assert chain_with_blocks.find_block_by_index(50) is None