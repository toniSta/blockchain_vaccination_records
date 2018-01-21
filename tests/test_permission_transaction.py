from Crypto.PublicKey import RSA
from blockchain.transaction.permission_transaction import Permission, PermissionTransaction
import blockchain.helper.cryptography as crypto

import pytest
import os


PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())


@pytest.fixture()
def unsigned_tx():
    tx = PermissionTransaction(requested_permission=Permission.doctor, sender_pubkey=PUBLIC_KEY, timestamp=1234, version=1)
    yield tx


@pytest.fixture()
def signed_tx():
    tx = PermissionTransaction(requested_permission=Permission.doctor, sender_pubkey=PUBLIC_KEY, timestamp=1234, version=1)
    tx.sign(PRIVATE_KEY)
    yield tx


@pytest.fixture()
def approvals():
    admission1 = crypto.generate_keypair()
    admission2 = crypto.generate_keypair()
    admission3 = crypto.generate_keypair()
    pubkey1 = admission1[0].exportKey("DER")
    pubkey2 = admission2[0].exportKey("DER")
    pubkey3 = admission3[0].exportKey("DER")
    approval1 = (pubkey1, crypto.sign(pubkey1, admission1[1]))
    approval2 = (pubkey2, crypto.sign(pubkey2, admission2[1]))
    approval3 = (pubkey3, crypto.sign(pubkey3, admission3[1]))
    fake_approval = (pubkey3, b"asdf")
    yield approval1, approval2, approval3, fake_approval


def test_transaction_representation(unsigned_tx):
    representation = repr(unsigned_tx)
    assert representation == "PermissionTransaction(approvals=[], requested_permission=Permission.doctor, sender_pubkey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', signature=None, timestamp=1234, version=1)"
    assert str(eval(representation)) == \
 """-----------------------
  Transaction: PermissionTransaction
  Approvals: []
  Requested_Permission: Permission.doctor
  Sender_Pubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Signature: None
  Timestamp: 1234
  Version: 1
-----------------------"""


def test_signed_transaction_representation(signed_tx):
    representation = repr(signed_tx)
    assert representation == "PermissionTransaction(approvals=[], requested_permission=Permission.doctor, sender_pubkey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', signature=b'o\\xb0r\\xca\\xaf\\x1f\\xcc\\xf0O)Z\\'f\"\\x90\\xbf\\x13\\x1a\\xc5m\\xa9v\"+\\x05\\xe3\\x8f\\xa2\\xd7;\\xb8/\\x8dK\\x12\\xf7\\x0e\\xa3^Y{\\xc6\\xb9\\xc9\\x130\\xdc\\xee?\\x9fbZ\\x7f\\xb6Yj\\xe4R]\\'y\\xe9\\x9f\\xb1\\xe1\\x03I\\x9b\\xe5{\\xe93\\x82[ \\x16\\x01\\'\\xeb\\xc3\\xcb\\x13\\x8bV{\\x92\\xa0\\xa4\\xea\\xf6v\\x19\\xfb\\xc8\\xb0\\xff\\xcf\\xd4\\xc0gk\\x17\\xf6pnh\\x87c\\x98\\xaaX\\x9f\\r\\xa7A\\x01\\x884\\r\\xe6\\xd6\\xfb\\xe44\\xbcv\\x03\\\\\\xb8\\xaa\\x1a\\x88\\xf8l\\x977\\x95\\x86)x\\x8bX\\xe9%2\\x0c\\xf0\\x9a\\xf9&J3\\xf2\\x19i\\xeb]\\x91&\\xc0Y\\xa4\\xf8\\x0c{\\x93c\\xd4Fom\\xad\\x12\\x90\\xc7\\xb3P\\xf5\\x19\\xca\\xa1\\xba\\xc9\\x01\\xa79\\x9d\\xb7\\xcb\\x8e\\xcfe\\xb4\\xc7*\\x19\\xaf\\x84\\xae\\xb9\\x0f\\xf2z\\x1e8_*x\\\\*[\\x954[v8VnW\\xfe\\x13\\xf3\\xbb\\xdf\\xc6\\xdf\\xff\\x1d\\xb7\\xfd\\xbe\\xfb\\xd3xXr7\\xcf,>\\x12\\xee\\xc7\\xa2a$\\xe5\\xd0h5\\xc9@\\xda,^\\x83', timestamp=1234, version=1)"
    assert str(eval(representation)) == \
 """-----------------------
  Transaction: PermissionTransaction
  Approvals: []
  Requested_Permission: Permission.doctor
  Sender_Pubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Signature: 6fb072caaf1fccf04f295a27662290bf131ac56da976222b05e38fa2d73bb82f8d4b12f70ea35e597bc6b9c91330dcee3f9f625a7fb6596ae4525d2779e99fb1e103499be57be933825b20160127ebc3cb138b567b92a0a4eaf67619fbc8b0ffcfd4c0676b17f6706e68876398aa589f0da7410188340de6d6fbe434bc76035cb8aa1a88f86c9737958629788b58e925320cf09af9264a33f21969eb5d9126c059a4f80c7b9363d4466f6dad1290c7b350f519caa1bac901a7399db7cb8ecf65b4c72a19af84aeb90ff27a1e385f2a785c2a5b95345b7638566e57fe13f3bbdfc6dfff1db7fdbefbd378587237cf2c3e12eec7a26124e5d06835c940da2c5e83
  Timestamp: 1234
  Version: 1
-----------------------"""


def test_transaction_signing(unsigned_tx):
    unsigned_tx.sign(PRIVATE_KEY)
    assert unsigned_tx.signature.hex() == "6fb072caaf1fccf04f295a27662290bf131ac56da976222b05e38fa2d73bb82f8d4b12f70ea35e597bc6b9c91330dcee3f9f625a7fb6596ae4525d2779e99fb1e103499be57be933825b20160127ebc3cb138b567b92a0a4eaf67619fbc8b0ffcfd4c0676b17f6706e68876398aa589f0da7410188340de6d6fbe434bc76035cb8aa1a88f86c9737958629788b58e925320cf09af9264a33f21969eb5d9126c059a4f80c7b9363d4466f6dad1290c7b350f519caa1bac901a7399db7cb8ecf65b4c72a19af84aeb90ff27a1e385f2a785c2a5b95345b7638566e57fe13f3bbdfc6dfff1db7fdbefbd378587237cf2c3e12eec7a26124e5d06835c940da2c5e83"


def test_transaction_signature_verification(signed_tx):
    assert signed_tx._verify_signature() == True
    signed_tx.requested_permission = Permission.admission # tamper with the transaction
    assert signed_tx._verify_signature() == False, "signature check should return False on tampered transaction"


def test_transaction_validation(approvals):
    chain_size = 0  # mock empty chain
    current_admissions = set() # mock empty chain with no admissions
    approval1, approval2, approval3, fake_approval = approvals
    wallet = crypto.generate_keypair()
    tx1 = PermissionTransaction(Permission.patient, wallet[0])
    tx1.sign(wallet[1])
    assert tx1.validate(chain_size, current_admissions) == True, "patient permission should be granted when signed"
    tx2 = PermissionTransaction(Permission.doctor, wallet[0], [approval1, approval2])
    tx2.sign(wallet[1])
    # assert tx2.validate(chain_size, current_admissions) == False, "transaction need minimum number of approvals" TODO: put back in after implementing genesis
    tx3 = PermissionTransaction(Permission.doctor, wallet[0], [approval1, approval2, fake_approval])
    tx3.sign(wallet[1])
    assert tx3.validate(chain_size, current_admissions) == False, "transaction should not validate with tampered approvals"
    tx4 = PermissionTransaction(Permission.doctor, wallet[0], [approval1, approval1, approval1])
    tx4.sign(wallet[1])
    assert tx4.validate(chain_size, current_admissions) == False, "transaction should not validate with duplicate approvals"
    tx5 = PermissionTransaction(Permission.doctor, wallet[0], [approval1, approval2, approval3])
    tx5.sign(wallet[1])
    assert tx5.validate(chain_size, current_admissions) == True, "transaction matching the requirements should succesfully validate"
