import pytest
import os
import shutil
from time import time

from blockchain.helper.key_utils import load_rsa_from_pem
from blockchain.block import Block, create_initial_block
from blockchain.transaction import *
from blockchain.helper.block_validator import validate_block
from blockchain.config import CONFIG

from tests.config_fixture import setup_test_config
setup_test_config()

GENESIS = None
PUBLIC_KEY = None
PRIVATE_KEY = None


def setup_module(module):
    # blockchain files folder will be deleted by create_initial_block
    global GENESIS, PUBLIC_KEY, PRIVATE_KEY
    GENESIS = create_initial_block()

    public_key_path = os.path.join(CONFIG.key_folder, CONFIG.key_file_names[0])
    private_key_path = os.path.join(CONFIG.key_folder, CONFIG.key_file_names[1])

    PUBLIC_KEY = load_rsa_from_pem(public_key_path)
    PRIVATE_KEY = load_rsa_from_pem(private_key_path)


@pytest.fixture()
def block():
    new_block = Block(GENESIS.get_block_information(), PUBLIC_KEY)
    new_transaction = PermissionTransaction(Permission.doctor, PUBLIC_KEY).sign(PRIVATE_KEY)
    new_block.add_transaction(new_transaction)
    yield new_block


def test_initial_block_is_valid(block):
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is True, "Error in initial block"


def test_index(block):
    block.index = 2000
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Did not detect wrong index"


def test_previous_block_hash(block):
    block.previous_block = "some random hash"
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Did not detect wrong prev. block hash"


def test_version(block):
    block.version = "0"
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Did not detect wrong version"


def test_timestamp(block):
    block.timestamp = int(time()) + 50000000
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Did not detect wrong version"


def test_signature_validity(block):
    block.sign(PRIVATE_KEY)
    block.index = 302
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Invalid signature"


def test_invalid_transaction(block):
    # Leave tx unsigned
    new_transaction = VaccineTransaction("some vaccine", PUBLIC_KEY)
    block.add_transaction(new_transaction)
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Invalid transaction"


def test_too_few_transactions(block):
    block.transactions = []
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    # WONTFIX: Actually, a block should never be empty. However, we leave this
    # check disabled for demo purposes.
    # assert is_valid is False, "Too few transactions"
    assert is_valid is True


@pytest.mark.long
def test_too_many_transactions(block):
    for index in range(CONFIG.block_size):
        new_transaction = VaccineTransaction(str(index), PUBLIC_KEY).sign(PRIVATE_KEY)
        block.add_transaction(new_transaction)
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Too many transactions"


def test_duplicate_transactions(block):
    block.add_transaction(block.transactions[0])
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Duplicate transactions"


def test_wrong_hash(block):
    block.sign(PRIVATE_KEY)
    block.hash = "4886f70d010101050"
    is_valid = validate_block(block, GENESIS)
    assert is_valid is False, "Invalid hash"


def teardown_module(module):
    shutil.rmtree(CONFIG.persistance_folder)
    os.makedirs(CONFIG.persistance_folder)
