import shutil

from blockchain.helper import key_utils
from Crypto.PublicKey import RSA

import pytest
import os

TMP_DIR = os.path.abspath('tests/key_test')

def setup_module(module):
    shutil.rmtree(TMP_DIR, True)
    os.makedirs(TMP_DIR)

def teardown_module(module):
    pass #shutil.rmtree(TMP_DIR)

@pytest.fixture()
def public_key():
    with open("tests" + os.sep + "testkey_pub.bin", 'rb') as file:
        public_key = RSA.import_key(file.read())
    yield public_key

@pytest.fixture()
def public_key_bytes():
    with open("tests" + os.sep + "testkey_pub.bin", 'rb') as file:
        public_key_bytes = RSA.import_key(file.read()).exportKey('DER')
    yield public_key_bytes

@pytest.fixture()
def public_key_hex():
    with open("tests" + os.sep + "testkey_pub.bin", 'rb') as file:
        public_key_hex = RSA.import_key(file.read()).exportKey('DER').hex()
    yield public_key_hex

@pytest.fixture()
def private_key():
    with open("tests" + os.sep + "testkey_priv.bin", 'rb') as file:
        private_key = RSA.import_key(file.read())
    yield private_key

@pytest.fixture()
def private_key_bytes():
    with open("tests" + os.sep + "testkey_priv.bin", 'rb') as file:
        private_key_bytes = RSA.import_key(file.read()).exportKey('DER')
    yield private_key_bytes

@pytest.fixture()
def private_key_hex():
    with open("tests" + os.sep + "testkey_priv.bin", 'rb') as file:
        private_key_hex = RSA.import_key(file.read()).exportKey('DER').hex()
    yield private_key_hex


def test_bytes_to_rsa(public_key, private_key):
    rsa_object = key_utils.bytes_to_rsa(public_key.exportKey("DER"))
    assert rsa_object == public_key
    rsa_object = key_utils.bytes_to_rsa(private_key.exportKey("DER"))
    assert rsa_object == private_key

def test_bytes_to_hex(public_key_bytes, public_key_hex, private_key_bytes, private_key_hex):
    hex_object = key_utils.bytes_to_hex(public_key_bytes)
    assert hex_object == public_key_hex
    hex_object = key_utils.bytes_to_hex(private_key_bytes)
    assert hex_object == private_key_hex

def test_hex_to_bytes(public_key_bytes, public_key_hex, private_key_bytes, private_key_hex):
    object = key_utils.hex_to_bytes(public_key_hex)
    assert object == public_key_bytes
    object = key_utils.hex_to_bytes(private_key_hex)
    assert object == private_key_bytes

def test_hex_to_rsa(public_key, public_key_hex, private_key, private_key_hex):
    object = key_utils.hex_to_rsa(public_key_hex)
    assert object == public_key
    object = key_utils.hex_to_rsa(private_key_hex)
    assert object == private_key

def test_rsa_to_bytes(public_key, public_key_bytes, private_key, private_key_bytes):
    object = key_utils.rsa_to_bytes(public_key)
    assert object == public_key_bytes
    object = key_utils.rsa_to_bytes(private_key)
    assert object == private_key_bytes

def test_rsa_to_hex(public_key, public_key_hex, private_key, private_key_hex):
    object = key_utils.rsa_to_hex(public_key)
    assert object == public_key_hex
    object = key_utils.rsa_to_hex(private_key)
    assert object == private_key_hex

def test_cast_to_bytes(public_key, public_key_hex, public_key_bytes, private_key, private_key_hex, private_key_bytes):
    object = key_utils.cast_to_bytes(public_key)
    assert object == public_key_bytes
    object = key_utils.cast_to_bytes(public_key_bytes)
    assert object == public_key_bytes
    object = key_utils.cast_to_bytes(public_key_hex)
    assert object == public_key_bytes

    object = key_utils.cast_to_bytes(private_key)
    assert object == private_key_bytes
    object = key_utils.cast_to_bytes(private_key_bytes)
    assert object == private_key_bytes
    object = key_utils.cast_to_bytes(private_key_hex)
    assert object == private_key_bytes

    with pytest.raises(ValueError):
        key_utils.cast_to_bytes(1234)

def test_write_key_to_pem(public_key, public_key_hex, public_key_bytes, private_key, private_key_hex, private_key_bytes):
    file_path = os.path.join(TMP_DIR, 'test')
    key_utils.write_key_to_pem(private_key, file_path)
    with open(file_path, 'rb') as file:
        assert file.readline().strip() == b'-----BEGIN RSA PRIVATE KEY-----'
    os.remove(file_path)
    key_utils.write_key_to_pem(private_key_bytes, file_path)
    with open(file_path, 'rb') as file:
        assert file.readline().strip() == b'-----BEGIN RSA PRIVATE KEY-----'
    os.remove(file_path)
    key_utils.write_key_to_pem(private_key_hex, file_path)
    with open(file_path, 'rb') as file:
        assert file.readline().strip() == b'-----BEGIN RSA PRIVATE KEY-----'
    os.remove(file_path)

    key_utils.write_key_to_pem(public_key_hex, file_path)
    with open(file_path, 'rb') as file:
        assert file.readline().strip() == b'-----BEGIN PUBLIC KEY-----'
    os.remove(file_path)
    key_utils.write_key_to_pem(public_key_bytes, file_path)
    with open(file_path, 'rb') as file:
        assert file.readline().strip() == b'-----BEGIN PUBLIC KEY-----'
    os.remove(file_path)
    key_utils.write_key_to_pem(public_key, file_path)
    with open(file_path, 'rb') as file:
        assert file.readline().strip() == b'-----BEGIN PUBLIC KEY-----'
    os.remove(file_path)
