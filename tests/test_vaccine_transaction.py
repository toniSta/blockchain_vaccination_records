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
    assert representation == "VaccineTransaction(signature=b'[Te\\x9f\\x95\\xb7e\\xbb\\x1e\\xa1\\x85\\xf5\\xfau^\\x16\\xd3\\xe9M\\x17\\xfe\\xe1\\x11(\\xddb\\r\\xc5\\xe1\\xfaJB\\x12k;Z\\x88h\\x114\\x14 \\x83\\xcdj\\r\\x06S\\x0c\\x8e\\x89\\xf2\\xdf\\x9cH}\\xd6\\x92\\xf0\\x04)\\xc2Sh\"-\\x11\\xf8\\xc5f\\xe7\\x97\\x02r\\x98\\x86\\xcfW.?1&\\xfc\\xbc]\\x91\\x8c\\xa3\\xbe\\xb5s4\\x04\\xa1\\xc4\\x0bCn\\xb0\\x94_\\xe2\"\\x80\\xfa\\x96\\xfd\\xdaI\\xd6\\x0fm/Kh\\xb97+\\xb1\\xd9Xq\\x1fj\\xb1\\x0b\\x9a\\x0eNj\\xc0\\xa5\\x8c\\x93\\tw\\x89\\xa4>\\x08\\xd6\\xf4\\x1e\\x87\\xa4\\xbd\\xae\\x9e\\x0bZ\\xe5\\xf7\\xd5Z\\xb8\\xccW\\xc0\\x87h\\xb5\\\\\\x8cB\\xd8\\xcf\\xe3\\xa4_\\xfb2^\\xba\\xa2\\xb5u\\x83,2\\xe5\\xa5\\x03$\\xb0\\x10\\x15N\\xfe\\xd2*EPk\\xa1\\xc9\\x86\\xee\\x17Z\\xdca\\n\\x05\\xe9%\\xf0\\x0e4\\'\\xc8\\x918\\xd4,\\x04%\\x8b\\xc0k\\x8c\\x07\\xc8\\xeb\\xc7\\xdfd\\xa30\\xf3@\\xe0\\x1e\\x02\\x17\\xcd\\xec\\x1f\\xae\\x84^\\xc6\\xff}V\\xb0\\x13\\xf8\"\\xec\\x1f8[\\xf5\\xfa\\xbc\\x06', timestamp=1234, vaccine='a vaccine', version='1')"
    assert str(eval(representation)) == \
"""-----------------------
  Transaction: VaccineTransaction
  Signature: 5b54659f95b765bb1ea185f5fa755e16d3e94d17fee11128dd620dc5e1fa4a42126b3b5a88681134142083cd6a0d06530c8e89f2df9c487dd692f00429c25368222d11f8c566e79702729886cf572e3f3126fcbc5d918ca3beb5733404a1c40b436eb0945fe22280fa96fdda49d60f6d2f4b68b9372bb1d958711f6ab10b9a0e4e6ac0a58c93097789a43e08d6f41e87a4bdae9e0b5ae5f7d55ab8cc57c08768b55c8c42d8cfe3a45ffb325ebaa2b575832c32e5a50324b010154efed22a45506ba1c986ee175adc610a05e925f00e3427c89138d42c04258bc06b8c07c8ebc7df64a330f340e01e0217cdec1fae845ec6ff7d56b013f822ec1f385bf5fabc06
  Timestamp: 1234
  Vaccine: a vaccine
  Version: 1
-----------------------"""

def test_transaction_signature_verification(signed_tx):
    assert signed_tx.validate(PUBLIC_KEY) == True
    signed_tx.vaccine = 'another vaccine' # tamper with the transaction
    assert signed_tx.validate(PUBLIC_KEY) == False, "signature check should return False on tampered transaction"