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
    assert representation == "PermissionTransaction(requested_permission=Permission.doctor, sender_pubkey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', signature=b'\\x95&z\\xa9\\xb4\\r\\xa2\\x8cx\\x84$l\\xc2\\xfb*\\x0f\\xa9\\x1ef\\xe7\\xd8\\x82\\xe95\\x7fv\\xf5q\\xe4\\xb11\\xdf\\xa2\\x97\\x86\\xfbe{!\\xf2P,\\x93Z\\xf6`7\\x0b\\xf4s\\xb9\\xc6\\x8f\\x1b\\x96y\\xe4\\xefL\\xbf\\xcfJ#8\\x7f\\x80:o\\x18\\x0cg\\x02\\x18r\\xe1o\\t\\xc2\\xbd\\x88q\\x85{\\xd1\\xb0o\\xf0Gb\\xaf0f\\xa5\\xadP\\x93\\x81^\\x8c\\xbf\\t\\\\\\xc7\\xea\\x94\\xb8\\xe0\\xa8I2w=\\xa8YK ?\\xf5\\xf9\\xc8\\xa6\\xcd<\\x9fI\\xb36 \\xd4\\xe6\\xbb-\\xf6s\\x92=P\\x1f|\\xdc\\x05\\xbc\\xd4\\xc6\\x89F\\xdcS\\xa8}hNo\\xdb\\xd0\\xa1i\\xf1e{\\x93\\xf7\\xeeV\\xcc\\xdc\\xaa\\xca\\x9f\\x9a?B\\xdf\\x9b\\x96X\\xae\\x19\\x81\\xd6\\x13h^&\\xc0D\\x84G\\x03t\\xe7\\x18\\xda0\\x9bB\\x8c\\xde\\x8d/r\\t\\x071\\xb8\\xd2\\xb8\\xb0\\xfd\\x0b\\x1fc\\xa9[\\x84\\x0f\\xac\\xc4\\xb8\\xcdv_\\xe5\\xe0w]\\xcc/<\\x025\\xae \\x1e(\\xb0)wO\\xb4\\x04WK{\\xa4~TP\\xdb\\xc9\\x97\\xa3\\xe8_<b', timestamp=1234, version=1)"
    assert str(eval(representation)) == \
 """-----------------------
  Transaction: PermissionTransaction
  Requested_Permission: Permission.doctor
  Sender_Pubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Signature: 95267aa9b40da28c7884246cc2fb2a0fa91e66e7d882e9357f76f571e4b131dfa29786fb657b21f2502c935af660370bf473b9c68f1b9679e4ef4cbfcf4a23387f803a6f180c67021872e16f09c2bd8871857bd1b06ff04762af3066a5ad5093815e8cbf095cc7ea94b8e0a84932773da8594b203ff5f9c8a6cd3c9f49b33620d4e6bb2df673923d501f7cdc05bcd4c68946dc53a87d684e6fdbd0a169f1657b93f7ee56ccdcaaca9f9a3f42df9b9658ae1981d613685e26c04484470374e718da309b428cde8d2f72090731b8d2b8b0fd0b1f63a95b840facc4b8cd765fe5e0775dcc2f3c0235ae201e28b029774fb404574b7ba47e5450dbc997a3e85f3c62
  Timestamp: 1234
  Version: 1
-----------------------"""

def test_transaction_signing(tx):
    tx.sign(PRIVATE_KEY)
    assert tx.signature.hex() == "95267aa9b40da28c7884246cc2fb2a0fa91e66e7d882e9357f76f571e4b131dfa29786fb657b21f2502c935af660370bf473b9c68f1b9679e4ef4cbfcf4a23387f803a6f180c67021872e16f09c2bd8871857bd1b06ff04762af3066a5ad5093815e8cbf095cc7ea94b8e0a84932773da8594b203ff5f9c8a6cd3c9f49b33620d4e6bb2df673923d501f7cdc05bcd4c68946dc53a87d684e6fdbd0a169f1657b93f7ee56ccdcaaca9f9a3f42df9b9658ae1981d613685e26c04484470374e718da309b428cde8d2f72090731b8d2b8b0fd0b1f63a95b840facc4b8cd765fe5e0775dcc2f3c0235ae201e28b029774fb404574b7ba47e5450dbc997a3e85f3c62"

def test_transaction_signature_verification(signed_tx):
    assert signed_tx._verify_signature() == True
    signed_tx.requested_permission = Permission.admission # tamper with the transaction
    assert signed_tx._verify_signature() == False, "signature check should return False on tampered transaction"

def test_transaction_validation():
    pass
