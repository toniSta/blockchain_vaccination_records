from blockchain.block import Block, create_initial_block

import pytest


@pytest.fixture()
def genesis():
    genesis = create_initial_block()
    genesis.update_hash()
    yield genesis


def test_genesis_block_header(genesis):
    assert genesis.index == 0, 'Index of genesis must be 0'
    assert genesis.previous_block == str(0), 'Genesis has no previous block'


@pytest.fixture()
def new_block(genesis):
    new_block = Block(genesis.get_block_information())
    new_block.add_transaction('tx1')
    new_block.add_transaction('tx2')
    new_block.update_hash()
    yield new_block


def test_new_block_references_old_one(genesis, new_block):
    assert new_block.previous_block == genesis.hash,\
        "New block does not reference previous one"
    assert new_block.merkle_root == genesis.merkle_root,\
        "Merkle is always the same"


def test_serialization_deserialization(new_block):
    assert type(repr(new_block)) == str,\
        "Object representation must be string"
    assert repr(new_block) == repr(Block(repr(new_block))),\
        "After serialization + de-serialization, block must have same content"
