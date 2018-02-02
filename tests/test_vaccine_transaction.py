from Crypto.PublicKey import RSA
from blockchain.transaction.vaccine_transaction import VaccineTransaction

import pytest
import os


PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())

@pytest.fixture()
def tx():
    tx = VaccineTransaction(vaccine='a vaccine', sender_pubkey=PUBLIC_KEY, timestamp=1234, version='1')
    yield tx

@pytest.fixture()
def signed_tx():
    tx = VaccineTransaction(vaccine='a vaccine', sender_pubkey=PUBLIC_KEY, timestamp=1234, version='1')
    tx.sign(PRIVATE_KEY)
    yield tx

def test_representation(signed_tx):
    representation = repr(signed_tx)
    assert representation == "VaccineTransaction(sender_pubkey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', signature=b'\\xa6\\xf9?\\x10\\x8a\\xb7vJ\\x18B\\xd6\\xa44m\\x8aip/\\xed\\xc9(\\x13\\x0f\\xae\\x14>l\\xee\\xedR\\x0cE\\xf7\\x98\\x94`\\xd8\\xc0>\\xc7~\\xd5>jQ\\xcd\\xc3,\\xd0\\xc1\\xeb\\xb5\\xc0[8\\xf6v\\xef\\x0b\\xf0W\\x0c\\xee\\x92\\xf4B\\xba\\xc4\\xc0\\xb8g\\xa0\\xca\\xb9\\xec\\xf5\\x7fq\\xa8\\xc9;9\\xd2S\\x8b\\x19\\xa6\\x9a>[\\x08\\xce@sl\\xd6\\xf69\\xf4}OxX\\x19`\\xfdD\\t\\xd1\\xc2\\\\y.\\xda\\x92\\x05\\x1b\\xe2*z\\xcb\\xcdK\\x93\\xd2\\xa7k2=\\xfeX\\xfa\\xbd\\xec\\xdd\\xe3K6\\xd2\\xd9\\xffm\\x9a\\xf1\\xed\\xcf\\x00\\x89\\xc1\\x98\\xd2\\xb6\\xb5b\\xb2\\xc9\\x9cL\\x1a-.2\\xf3J\\xfa\\xa4\\x89\\x8a\\x95\\xf9A\\xf9uq\\\\\\xe5jS\\xbf\\xa5A\\x03\\x06 \\xdf\\x9f\\xad\\xdc\\x06\\x96\\r\\x8a\\xa1\\x8f\\xa8\\x93\\xb8rD\\x1f\\x00\\xf1\\xa4\\x02\\xd5\\xfe9GL\\xb8\\x8d\\xe4\"\\xcb\\xe69\\x9e4\\x96}\\xf5\\x84\\x824hx\\xc4\\xfavZ\\xe9\\x9f\\x92\\xb0$\\xf4\\xc2\\x05I\\xcd\\xb9\\xb5$\\x1dW\\ns\\xd4v\\x9e;\\x8eW\\xd3\\xbc\\xeb', timestamp=1234, vaccine='a vaccine', version='1')"
    assert str(eval(representation)) == \
"""-----------------------
  Transaction: VaccineTransaction
  Sender_Pubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Signature: a6f93f108ab7764a1842d6a4346d8a69702fedc928130fae143e6ceeed520c45f7989460d8c03ec77ed53e6a51cdc32cd0c1ebb5c05b38f676ef0bf0570cee92f442bac4c0b867a0cab9ecf57f71a8c93b39d2538b19a69a3e5b08ce40736cd6f639f47d4f78581960fd4409d1c25c792eda92051be22a7acbcd4b93d2a76b323dfe58fabdecdde34b36d2d9ff6d9af1edcf0089c198d2b6b562b2c99c4c1a2d2e32f34afaa4898a95f941f975715ce56a53bfa541030620df9faddc06960d8aa18fa893b872441f00f1a402d5fe39474cb88de422cbe6399e34967df58482346878c4fa765ae99f92b024f4c20549cdb9b5241d570a73d4769e3b8e57d3bceb
  Timestamp: 1234
  Vaccine: a vaccine
  Version: 1
-----------------------"""

def test_transaction_signature_verification(signed_tx):
    current_admissions = set()  # mock empty chain with no admissions
    current_admissions.add(signed_tx.sender_pubkey)
    doctors = set()  # mock registered doctors
    vaccines = set()  # mock registered vaccines
    assert signed_tx.validate(current_admissions, doctors, vaccines) == True
    signed_tx.vaccine = 'another vaccine' # tamper with the transaction
    assert signed_tx.validate(current_admissions, doctors, vaccines) == False, "signature check should return False on tampered transaction"
