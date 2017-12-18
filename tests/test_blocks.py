from blockchain.block import Block, create_initial_block

import pytest


@pytest.fixture()
def resource():
    genesis = create_initial_block()
    genesis.update_hash()
    yield genesis


def test_genesis_block_header(resource):
    assert resource.index == 0, 'Index of genesis must be 0'
    assert resource.previous_block == 0, 'Genesis has no previous block'


def test_new_block_references_old_one(resource):
    new_block = Block(resource.get_block_information())
    assert new_block.previous_block == resource.hash,\
        "New block does not reference previous one"
    assert new_block.merkle == resource.merkle, "Merkle is always the same"
