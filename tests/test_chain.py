import shutil

# noinspection PyUnresolvedReferences
from time import sleep

from blockchain.full_client import FullClient
from blockchain.chain import Chain
from blockchain.block import Block, create_initial_block
from blockchain.config import CONFIG
from blockchain.helper.key_utils import load_rsa_from_pem

import pytest
import os

from tests.config_fixture import setup_test_config
setup_test_config()

PUBLIC_KEY = load_rsa_from_pem("tests" + os.sep + "testkey_pub.bin")
PRIVATE_KEY = load_rsa_from_pem("tests" + os.sep + "testkey_priv.bin")


def setup_module(module):
    shutil.rmtree(CONFIG.persistance_folder, True)
    os.makedirs(CONFIG.persistance_folder)


def test_chain_is_singleton():
    chain_1 = Chain(load_persisted=False)
    chain_2 = Chain(load_persisted=False)
    assert id(chain_1) == id(chain_2)


@pytest.fixture(scope="session")
def chain():
    chain = Chain(load_persisted=False)
    genesis = create_initial_block()
    chain.add_block(genesis)
    yield chain


@pytest.fixture(scope="session")
def next_block(chain):
    block_information = chain.genesis_block.get_block_information()
    next_block = Block(block_information, PUBLIC_KEY)
    next_block.sign(PRIVATE_KEY)
    next_block.update_hash()
    yield next_block

@pytest.fixture(scope="session")
def next_next_block(chain):
    block_information = chain.genesis_block.get_block_information()
    sleep(CONFIG.block_time + 1)
    next_next_block = Block(block_information, PUBLIC_KEY)
    next_next_block.sign(PRIVATE_KEY)
    next_next_block.update_hash()
    yield next_next_block

def test_add_block(chain, next_block, next_next_block):
    set = chain.add_block(next_next_block)
    hash = next_next_block.hash
    assert chain.find_block_by_hash(hash) == next_next_block
    assert len(set) == 0
    set = chain.add_block(next_block)
    hash = next_block.hash
    assert chain.find_block_by_hash(hash) == next_block
    assert len(set) == 1

def test_find_block_by_hash(chain, next_block):
    hash = next_block.hash
    assert chain.find_block_by_hash(hash) == next_block
    assert chain.find_block_by_hash("some random hash") is None




def teardown_module(module):
    shutil.rmtree(CONFIG.persistance_folder, True)
