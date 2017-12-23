from Crypto.PublicKey import RSA
from blockchain.cryptography import generate_keypair
from blockchain.permission_transaction import Permission, PermissionTransaction

import pytest
import os


PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())

@pytest.fixture()
def tx():
    tx = PermissionTransaction(Permission.doctor, PUBLIC_KEY)
    tx.timestamp = 12345 # override timestamp to allow signature checks
    yield tx

@pytest.fixture()
def signed_tx():
    tx = PermissionTransaction(Permission.doctor, PUBLIC_KEY)
    tx.timestamp = 12345 # override timestamp to allow signature checks
    tx.sign(PRIVATE_KEY)
    yield tx

def test_transaction_information(tx):
    info = tx.get_transaction_information()
    assert info["requested_permission"] == Permission.doctor, "Permission should request Doctor permissions"
    assert info["sender_wallet"] == PUBLIC_KEY.exportKey("DER"), "Sender public key must match wallet public key"
    assert info["signature"] == None, "Transaction should be unsigned on creation"

def test_signed_transaction_information(signed_tx):
    info = signed_tx.get_transaction_information()
    assert info["requested_permission"] == Permission.doctor, "Permission should request Doctor permissions"
    assert info["sender_wallet"] == PUBLIC_KEY.exportKey("DER"), "Sender public key must match wallet public key"
    assert info["signature"].hex() == "718644eceb969e331bb66113811770af71d3d522742a88e17804224b158a3b0e70857ff7415be7cfff39d23ae680af1cac0161b4786ca4ba7408122423667d598870623d04f1150efab17e55c0b2a38d00980be6afdea430f14542abe15fc43a3b621af56469cd84407df07c6c6eb4f18e302bbe6efc8670e58c660bf0359d9b473288cddc3430a57eb003aff24ab1e5677f938c2d20a96f74dae2cdae35313518642a609a9cbec931fba4e2fe98f3bd88093e26460418c3d9263aad43848ff1f2b58222ad176fb177a895c10134c3b2c62d4e8e18bda86756065ecc9409b8494257daa4f63d9d133a1d3d7473185eb0896f5b5ed26cd5831b02f8bc5a719b69"

def test_transaction_signing(tx):
    tx.sign(PRIVATE_KEY)
    assert tx.signature.hex() == "718644eceb969e331bb66113811770af71d3d522742a88e17804224b158a3b0e70857ff7415be7cfff39d23ae680af1cac0161b4786ca4ba7408122423667d598870623d04f1150efab17e55c0b2a38d00980be6afdea430f14542abe15fc43a3b621af56469cd84407df07c6c6eb4f18e302bbe6efc8670e58c660bf0359d9b473288cddc3430a57eb003aff24ab1e5677f938c2d20a96f74dae2cdae35313518642a609a9cbec931fba4e2fe98f3bd88093e26460418c3d9263aad43848ff1f2b58222ad176fb177a895c10134c3b2c62d4e8e18bda86756065ecc9409b8494257daa4f63d9d133a1d3d7473185eb0896f5b5ed26cd5831b02f8bc5a719b69"

def test_transaction_signature_verification(signed_tx):
    assert signed_tx._verify_signature() == True
    signed_tx.requested_permission = Permission.admission # tamper with the transaction
    assert signed_tx._verify_signature() == False, "signature check should return False on tampered transaction"

def test_transaction_validation():
    pass
