from Crypto.PublicKey import RSA
from blockchain.transaction.permission_transaction import Permission, PermissionTransaction

import pytest
import os


PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())

@pytest.fixture()
def tx():
    tx = PermissionTransaction(requested_permission=Permission.doctor, sender_pubkey=PUBLIC_KEY, timestamp=1234, version=1)
    yield tx

@pytest.fixture()
def signed_tx():
    tx = PermissionTransaction(requested_permission=Permission.doctor, sender_pubkey=PUBLIC_KEY, timestamp=1234, version=1)
    tx.sign(PRIVATE_KEY)
    yield tx


def test_transaction_representation(tx):
    representation = repr(tx)
    assert representation == "PermissionTransaction(requested_permission=Permission.doctor, sender_pubkey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', signature=None, timestamp=1234, version=1)"
    assert str(eval(representation)) == \
 """-----------------------
  Transaction: PermissionTransaction
  Requested_Permission: Permission.doctor
  Sender_Pubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Signature: None
  Timestamp: 1234
  Version: 1
-----------------------"""

def test_signed_transaction_representation(signed_tx):
    representation = repr(signed_tx)
    print(representation)
    print(signed_tx)
    assert representation == "PermissionTransaction(requested_permission=Permission.doctor, sender_pubkey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', signature=b']a}\\x80*\\x8f9\\xde\\xf2\\x83\\x82\\xe9\\xd3\\xbe\\xbcWB\\x8b\\\\\\x95r.\\xcd\\x93\\x00z\\xa96o\\xb4\\xc8&\\xf1,\\x94\\x85\\xfd\\xdd\\xe4\\x01\\x1c\\xcb\\xa2w\\xa5\\xa7\\xa7>\\x84\\x83z\\x0b\\x9d\\xf6mkx\\x85\\xa6/\\xf0;\\x8b\\x00\\x92\\x9c\\xb6o\\x82\\xd4nm\\xcfl\\xde>\\xcd\\x9bQ\\xc4\\x8b\\xf2\\x14\\xef\\x19\\xdf\\x9b\\x99\\x0b\\x1e\\x92\\xc8\"\\xeb\\xca\\x16\\x12\\xc8PG\\x97\\x93\\xf5\\xe3%\\xc4M\\xfc\\x93\\x8a\\xbe;\\xbf\\xb7?&\\xd8\\xe0\\x1fzx8\\x95\\x1d\\xce\\x18\\xac\\ti\\xa1\\x85\\xbdy\\x0c\\xd7\\xdb\\x0c\\x81\\x9cC\\xb6T\\xde\\x14\\x83\\'\\xff\\xac+\\x9d\\r\\xc5\\x14\\xc0U\\x1c\\x89Zb\\xef\\xc0Fu\\xdd\\x9b\\xbb;=H\\x9f\\x8d\\xca\\x04Co\\x12\\xce\\x03\\x8c\\x069]\\x11<\\xf6\\xa5\\'\\x13^\\x17\\xaau\\xbd\\xc0@\\xc18\\x00\\xa9>\\x16z\\xc2\\x05]i\\xf30\\xe9\\x04\\x89\\xa3\\x06P\\xee]\\xaf\\x8e\\xec\\xdb\\xe6\\xed\\x8d\\x9a\\n\\x91m\\x8a\\x9a\\r~y\\xbc\\xba%\\xb9Mf\\xd7]=u\\xb6\\xa7\\x88\\xa5\\xde\\xe2\\x89\\x92D<e\\xeag\\x8f', timestamp=1234, version=1)"
    assert str(eval(representation)) == \
"""-----------------------
  Transaction: PermissionTransaction
  Requested_Permission: Permission.doctor
  Sender_Pubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Signature: 5d617d802a8f39def28382e9d3bebc57428b5c95722ecd93007aa9366fb4c826f12c9485fddde4011ccba277a5a7a73e84837a0b9df66d6b7885a62ff03b8b00929cb66f82d46e6dcf6cde3ecd9b51c48bf214ef19df9b990b1e92c822ebca1612c850479793f5e325c44dfc938abe3bbfb73f26d8e01f7a7838951dce18ac0969a185bd790cd7db0c819c43b654de148327ffac2b9d0dc514c0551c895a62efc04675dd9bbb3b3d489f8dca04436f12ce038c06395d113cf6a527135e17aa75bdc040c13800a93e167ac2055d69f330e90489a30650ee5daf8eecdbe6ed8d9a0a916d8a9a0d7e79bcba25b94d66d75d3d75b6a788a5dee28992443c65ea678f
  Timestamp: 1234
  Version: 1
-----------------------"""

def test_transaction_signing(tx):
    tx.sign(PRIVATE_KEY)
    assert tx.signature.hex() == "5d617d802a8f39def28382e9d3bebc57428b5c95722ecd93007aa9366fb4c826f12c9485fddde4011ccba277a5a7a73e84837a0b9df66d6b7885a62ff03b8b00929cb66f82d46e6dcf6cde3ecd9b51c48bf214ef19df9b990b1e92c822ebca1612c850479793f5e325c44dfc938abe3bbfb73f26d8e01f7a7838951dce18ac0969a185bd790cd7db0c819c43b654de148327ffac2b9d0dc514c0551c895a62efc04675dd9bbb3b3d489f8dca04436f12ce038c06395d113cf6a527135e17aa75bdc040c13800a93e167ac2055d69f330e90489a30650ee5daf8eecdbe6ed8d9a0a916d8a9a0d7e79bcba25b94d66d75d3d75b6a788a5dee28992443c65ea678f"

def test_transaction_signature_verification(signed_tx):
    assert signed_tx._verify_signature() == True
    signed_tx.requested_permission = Permission.admission # tamper with the transaction
    assert signed_tx._verify_signature() == False, "signature check should return False on tampered transaction"

def test_transaction_validation():
    pass
