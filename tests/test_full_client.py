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

def setup_module(module):
    shutil.rmtree(CONFIG.persistance_folder, True)
    os.makedirs(CONFIG.persistance_folder)
    create_initial_block().persist()
    global PUBLIC_KEY, PRIVATE_KEY
    PUBLIC_KEY = load_rsa_from_pem(os.path.join("tests", "keys", "public_key.bin"))
    PRIVATE_KEY = load_rsa_from_pem(os.path.join("tests", "keys", "private_key.bin"))

def teardown_module(module):
    pass#shutil.rmtree(CONFIG.persistance_folder, True)

@pytest.fixture(scope="module")
def full_client():
    Chain(init=True)
    full_client = FullClient()
    yield full_client

def test_received_new_block(full_client):
    block_information = full_client.chain.genesis_block.get_block_information()
    next_block = Block(block_information, PUBLIC_KEY)
    next_block.sign(PRIVATE_KEY)
    next_block.update_hash()
    full_client.received_new_block(repr(next_block))
    assert os.path.exists(os.path.join(CONFIG.persistance_folder,
                                       "_".join([str(next_block.index), next_block.previous_block, next_block.hash])))
