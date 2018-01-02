from Crypto.PublicKey import RSA
from blockchain.transaction.vaccine_transaction import VaccineTransaction

import pytest
import os


PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())

@pytest.fixture()
def tx():
    tx = VaccineTransaction(vaccine='a vaccine', timestamp=1234, version='1')
    yield tx

@pytest.fixture()
def signed_tx():
    tx = VaccineTransaction(vaccine='a vaccine', timestamp=1234, version='1')
    tx.sign(PRIVATE_KEY)
    yield tx

def test_representation(signed_tx):
    representation = repr(signed_tx)
    assert representation == "VaccineTransaction(signature=b\"\\x8f)\\xc0\\xb6q\\xac\\x1d\\xec\\xa7\\x18J,\\xf6\\xf0]\\xf4,5e\\xc9\\xd7\\x89J\\xfc\\x16\\x01\\xa6E\\x0bO\\xe7\\xb9\\xcb\\x0b\\xe0%\\x13\\xe5\\x0b\\x89\\x06\\x1bi\\xea]\\xfeJg\\x7f\\xe0\\xed\\x93v\\xdet\\xdc\\x8c\\x16r\\xc6\\xd4j\\x13\\x08\\xb8;b\\xd8\\x12\\xeb\\x80N\\xfd\\xf2l\\x90\\xa7\\x05*\\xd4WDS{\\xff4m1\\xcd\\xc2Tl\\x91\\x12@\\x83\\x87\\x11\\xa6Q\\xf5\\xb6\\xa7\\x8a=)i\\xfc,~\\xa0\\xb5'\\xeb$\\xb8b9\\xe2\\xbb\\x8e\\x8e\\xbd\\xc5\\x04:m\\xa7\\x0bb\\x86\\xff\\xd4Dk,1\\x02\\x18\\tby\\xf2\\xa8\\xef\\x8am8J\\xfd\\xae\\xa3\\x04D\\x1b\\xb8o# \\xc1\\x13\\xddh'\\xdd\\xfc,SJ\\xe79nuJ\\x002\\xbf\\x0b\\xcb\\x9bK`\\xa7\\x03\\x1c\\xe8rX\\xf6k\\xc3\\xe0\\x19\\x851\\xaeR\\x86\\x1a~c\\xa9\\x10\\x1d\\x16\\xee\\xa3\\xd7\\x13+\\x9e\\x80\\xba\\xbf\\xf2Y\\xb3\\x91\\xaf<\\xe9M\\xabz\\xd9iBf\\x1b\\xf7\\xd3\\xf8Lb}\\x03\\xa2\\x06\\xe2>\\xe6%0~4\\xe4\\xeb\\xa2$\\xe3\\xc2\\xe5\\xef\\xca\\xdb\\x8c\", timestamp=1234, vaccine='a vaccine', version='1')"
    assert str(eval(representation)) == \
"""-----------------------
  Transaction: VaccineTransaction
  Signature: 8f29c0b671ac1deca7184a2cf6f05df42c3565c9d7894afc1601a6450b4fe7b9cb0be02513e50b89061b69ea5dfe4a677fe0ed9376de74dc8c1672c6d46a1308b83b62d812eb804efdf26c90a7052ad45744537bff346d31cdc2546c911240838711a651f5b6a78a3d2969fc2c7ea0b527eb24b86239e2bb8e8ebdc5043a6da70b6286ffd4446b2c310218096279f2a8ef8a6d384afdaea304441bb86f2320c113dd6827ddfc2c534ae7396e754a0032bf0bcb9b4b60a7031ce87258f66bc3e0198531ae52861a7e63a9101d16eea3d7132b9e80babff259b391af3ce94dab7ad96942661bf7d3f84c627d03a206e23ee625307e34e4eba224e3c2e5efcadb8c
  Timestamp: 1234
  Vaccine: a vaccine
  Version: 1
-----------------------"""

def test_transaction_signature_verification(signed_tx):
    assert signed_tx.validate(PUBLIC_KEY) == True
    signed_tx.vaccine = 'another vaccine' # tamper with the transaction
    assert signed_tx.validate(PUBLIC_KEY) == False, "signature check should return False on tampered transaction"