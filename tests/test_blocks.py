from blockchain.block import Block, create_initial_block

import pytest

PUBLIC_KEY = "123"

@pytest.fixture()
def genesis():
    genesis = create_initial_block(PUBLIC_KEY)
    yield genesis


def test_genesis_block_header(genesis):
    assert genesis.index == 0, "Index of genesis must be 0"
    assert genesis.previous_block == str(0), "Genesis has no previous block"


def test_creation_of_successor_block(genesis):
    assert Block(genesis.get_block_information(), PUBLIC_KEY),\
        "Error at creation of successor block"
    with pytest.raises(Exception) as excinfo:
        Block(tuple())
    assert excinfo.type == ValueError


def test_block_creation_with_wrong_input():
    with pytest.raises(Exception):
        Block("")
    with pytest.raises(Exception):
        Block({})


@pytest.fixture()
def new_block(genesis):
    new_block = Block(genesis.get_block_information(), PUBLIC_KEY)
    new_block.add_transaction("tx1")
    new_block.add_transaction("tx2")
    new_block.update_hash()
    yield new_block


def test_new_block_references_old_one(genesis, new_block):
    assert new_block.previous_block == genesis.hash,\
        "New block does not reference previous one"


def test_block_recreation(new_block):
    assert Block(repr(new_block)),\
        "Error at recreation of block by string representation"


def test_serialization_deserialization(new_block):
    assert type(repr(new_block)) == str,\
        "Object representation must be string"
    assert repr(new_block) == repr(Block(repr(new_block))),\
        "After serialization + de-serialization, block must have same content"
