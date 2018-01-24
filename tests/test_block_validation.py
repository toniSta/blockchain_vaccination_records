from Crypto.PublicKey import RSA
import pytest
import os

from blockchain.block import Block, create_initial_block
from blockchain.transaction import *
from blockchain.block_validator import validate
from blockchain.config import CONFIG


PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())


@pytest.fixture()
def genesis():
    genesis = create_initial_block(PUBLIC_KEY, PRIVATE_KEY)
    yield genesis


@pytest.fixture()
def block(genesis):
    new_block = Block(genesis.get_block_information(), PUBLIC_KEY)
    new_transaction = VaccineTransaction("a vaccine", PUBLIC_KEY).sign(PRIVATE_KEY)
    new_block.add_transaction(new_transaction)
    new_transaction = PermissionTransaction(Permission.doctor, PUBLIC_KEY).sign(PRIVATE_KEY)
    new_block.add_transaction(new_transaction)
    yield new_block


def test_initial_block_is_valid(block, genesis):
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate(block, genesis)
    assert is_valid is True, "Error in initial block"


def test_index(block, genesis):
    block.index = 2000
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate(block, genesis)
    assert is_valid is False, "Did not detect wrong index"


def test_previous_block_hash(block, genesis):
    block.previous_block = "some random hash"
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate(block, genesis)
    assert is_valid is False, "Did not detect wrong prev. block hash"


def test_version(block, genesis):
    block.version = "0"
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate(block, genesis)
    assert is_valid is False, "Did not detect wrong version"


def test_signature_validity(block, genesis):
    block.sign(PRIVATE_KEY)
    block.index = 302
    block.update_hash()
    is_valid = validate(block, genesis)
    assert is_valid is False, "Invalid signature"


@pytest.mark.long
def test_too_many_transactions(block, genesis):
    for index in range(CONFIG["block_size"]):
        new_transaction = VaccineTransaction(str(index), PUBLIC_KEY).sign(PRIVATE_KEY)
        block.add_transaction(new_transaction)
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate(block, genesis)
    assert is_valid is False, "Too many transactions"


def test_duplicate_transactions(block, genesis):
    block.add_transaction(block.transactions[0])
    block.sign(PRIVATE_KEY)
    block.update_hash()
    is_valid = validate(block, genesis)
    assert is_valid is False, "Duplicate transactions"


def test_wrong_hash(block, genesis):
    block.sign(PRIVATE_KEY)
    block.hash = "4886f70d010101050"
    is_valid = validate(block, genesis)
    assert is_valid is False, "Invalid hash"
