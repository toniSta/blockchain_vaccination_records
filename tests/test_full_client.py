import shutil

# noinspection PyUnresolvedReferences
from time import sleep, time

from blockchain.full_client import FullClient
from blockchain.chain import Chain
from blockchain.block import Block, create_initial_block
from blockchain.config import CONFIG
from blockchain.helper.key_utils import load_rsa_from_pem
from blockchain.transaction.permission_transaction import Permission, PermissionTransaction

import pytest
import os
from mock import patch

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
    shutil.rmtree(CONFIG.persistance_folder, True)
    os.makedirs(CONFIG.persistance_folder)


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


@pytest.fixture()
def signed_permission_tx():
    tx = PermissionTransaction(requested_permission=Permission.doctor,
                               sender_pubkey=PUBLIC_KEY,
                               timestamp=1234,
                               version=1)
    tx.sign(PRIVATE_KEY)
    yield tx


def test_new_transaction(full_client, signed_permission_tx):
    full_client.handle_incoming_transaction(repr(signed_permission_tx))
    assert len(full_client.transaction_set) == 1
    full_client.handle_incoming_transaction(repr(signed_permission_tx))
    assert len(full_client.transaction_set) == 1


def test_key_setup(full_client):
    shutil.rmtree(CONFIG.key_folder, True)
    full_client._setup_public_key()
    assert len(os.listdir(CONFIG.key_folder)) == 2


def test_create_next_block(full_client, signed_permission_tx):
    fake_signed_permission_tx = signed_permission_tx
    fake_signed_permission_tx.requested_permission = Permission.admission
    full_client.handle_incoming_transaction(repr(fake_signed_permission_tx))
    block_time = int(time())
    previous_block_hash = full_client.chain.genesis_block.hash
    new_block = full_client._create_next_block(previous_block_hash, block_time)
    full_client._submit_block(new_block)
    assert new_block.validate(full_client.chain.genesis_block)
    assert full_client._create_next_block(None, block_time) is None


def test_registration_as_admission(full_client):
    with patch.object(full_client, '_broadcast_new_transaction') as mock:
        full_client.register_self_as_admission()
        assert not mock.called, "should be admission already"


def test_neighbor_list(monkeypatch):
    fc1 = FullClient()
    assert fc1.nodes == ["http://127.0.0.1:9000"]
    monkeypatch.setenv('NEIGHBORS_HOST_PORT', "node1:9000,node2:9000")
    fc2 = FullClient()
    assert fc2.nodes == ["http://node1:9000", "http://node2:9000"]
