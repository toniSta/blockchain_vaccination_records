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


@pytest.fixture(scope="module")
def chain():
    chain = Chain(load_persisted=False, init=True)
    genesis = create_initial_block()
    chain.add_block(genesis)
    yield chain


def test_lock_state(chain):
    assert not chain.lock_state()
    with chain._lock:
        assert chain.lock_state()


@pytest.fixture(scope="module")
def next_block_branch1(chain):
    block_information = chain.genesis_block.get_block_information()
    next_block_branch1 = Block(block_information, PUBLIC_KEY)
    next_block_branch1.sign(PRIVATE_KEY)
    next_block_branch1.update_hash()
    yield next_block_branch1


@pytest.fixture(scope="module")
def next_block_branch2(chain):
    block_information = chain.genesis_block.get_block_information()
    next_block_branch2 = Block(block_information, PUBLIC_KEY)
    next_block_branch2.timestamp = chain.genesis_block.timestamp + CONFIG.block_time + 1
    next_block_branch2.sign(PRIVATE_KEY)
    next_block_branch2.update_hash()
    yield next_block_branch2


def test_add_block(chain, next_block_branch1, next_block_branch2):
    set = chain.add_block(next_block_branch2)
    hash = next_block_branch2.hash
    assert chain.find_block_by_hash(hash) == next_block_branch2
    assert len(set) == 0
    set = chain.add_block(next_block_branch1)
    hash = next_block_branch1.hash
    assert chain.find_block_by_hash(hash) == next_block_branch1
    assert len(set) == 1


def test_find_block_by_hash(chain, next_block_branch1):
    hash = next_block_branch1.hash
    assert chain.find_block_by_hash(hash) == next_block_branch1
    assert chain.find_block_by_hash("some random hash") is None


def test_get_leaves(chain, next_block_branch1, next_block_branch2):
    assert len(chain.get_leaves()) == 2
    assert next_block_branch1 in chain.get_leaves()
    assert next_block_branch2 in chain.get_leaves()


def test_blocks_by_index(chain, next_block_branch1, next_block_branch2):
    blocks = chain.find_blocks_by_index(1)
    block_hashes = [block.hash for block in blocks]
    assert next_block_branch1.hash in block_hashes
    assert next_block_branch2.hash in block_hashes
    assert chain.find_blocks_by_index(1000) is None


def test_get_first_branching_block(chain):
    block = chain.get_first_branching_block()
    assert chain.genesis_block == block


def test_get_parent_node(chain, next_block_branch2):
    parent = chain.get_parent_block_by_hash(next_block_branch2.hash)
    assert parent.hash == chain.genesis_block.hash


@pytest.fixture(scope="module")
def dangling_block(chain):
    dangling_block = Block({"index": 4, "hash": "ab1234"}, PUBLIC_KEY)
    dangling_block.timestamp = chain.genesis_block.timestamp + 2 * CONFIG.block_time + 1
    dangling_block.sign(PRIVATE_KEY)
    dangling_block.update_hash()
    chain.add_dangling_block(dangling_block)
    yield dangling_block


def test_get_list_of_dangling_blocks(chain, dangling_block):
    dangling_blocks = chain.get_list_of_dangling_blocks()
    assert len(dangling_blocks) == 1
    assert dangling_block.hash == dangling_blocks[0].hash


def test_get_dangling_block(chain, dangling_block):
    assert chain.is_block_dangling(dangling_block)
    hash = chain._get_dangling_node_by_hash(dangling_block.hash).name
    assert dangling_block.hash == hash


def test_string_representation(chain, next_block_branch1, next_block_branch2, dangling_block):
    string_representation = str(chain)
    assert next_block_branch1.hash in string_representation
    assert next_block_branch2.hash in string_representation
    assert dangling_block.hash not in string_representation


def test_remove_block_from_dangling_list(chain, dangling_block):
    chain._remove_block_from_dangling_list(dangling_block)
    assert len(chain.get_list_of_dangling_blocks()) == 0


@pytest.fixture(scope="module")
def next_next_block_branch2(chain, next_block_branch2):
    block_information = next_block_branch2.get_block_information()
    next_next_block_branch2 = Block(block_information, PUBLIC_KEY)
    next_next_block_branch2.timestamp = chain.genesis_block.timestamp + CONFIG.block_time + 1
    next_next_block_branch2.sign(PRIVATE_KEY)
    next_next_block_branch2.update_hash()
    chain.add_block(next_next_block_branch2)
    yield next_next_block_branch2


def test_block_creation_history(chain, next_next_block_branch2):
    creators = chain.get_block_creation_history_by_hash(3, next_next_block_branch2.hash)
    assert len(creators) == 3
    # Genesis was created by another node
    assert len(set(creators)) == 2
    creators = chain.get_block_creation_history_by_hash(5, next_next_block_branch2.hash)
    assert creators is None


def test_get_registration_caches(chain, next_block_branch1, next_next_block_branch2):
    caches = chain.get_registration_caches()
    assert len(caches) == 2, "not every leaf as a cache"

    blocks = list(zip(*caches))[0]
    assert next_block_branch1.hash in blocks
    assert next_next_block_branch2.hash in blocks

    assert len(caches[0][1]) == 2, "admission cache must contain two admissions"
    assert len(caches[0][2]) == 0, "doctor cache must be empty"
    assert len(caches[0][3]) == 0, "vaccine cache must be empty"


def test_block_file_removal(chain, next_block_branch2, next_next_block_branch2):
    next_block_branch2.persist()
    next_next_block_branch2.persist()
    file_name = "_".join([str(next_block_branch2.index),
                          next_block_branch2.previous_block,
                          next_block_branch2.hash])
    assert file_name in os.listdir(CONFIG.persistance_folder)
    node_to_remove = chain._generate_tree_node(next_block_branch2)
    chain._remove_tree_at_node(node_to_remove)
    assert file_name not in os.listdir(CONFIG.persistance_folder)


def teardown_module(module):
    shutil.rmtree(CONFIG.persistance_folder, True)
    os.makedirs(CONFIG.persistance_folder)
