from Crypto.PublicKey import RSA
from blockchain.transaction.vaccine_transaction import VaccineTransaction

import pytest
import os


PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())

@pytest.fixture()
def tx():
    tx = VaccineTransaction(vaccine='a vaccine', senderPubKey=PUBLIC_KEY, timestamp=1234, version='1')
    yield tx

@pytest.fixture()
def signed_tx():
    tx = VaccineTransaction(vaccine='a vaccine', senderPubKey=PUBLIC_KEY, timestamp=1234, version='1')
    tx.sign(PRIVATE_KEY)
    yield tx

def test_representation(signed_tx):
    representation = repr(signed_tx)
    assert representation == "VaccineTransaction(senderPubKey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', signature=b'x\\xfd\\xa6M|\\x85\\x89\\x86\\xbd\"\\xa8\\xd6\\xfc\\xa3\\xb4\\xcd{Y\\xed\\xf4\\xcf\\xb9\\xc9\\x02\\t<\\xe6\\x94\\xccG%\\xb2\\x89-(\\xe8\\xf3yD\\xef\\xb0\\xeb\\xa1\\x8d\\x13Y ZI^\\x85\\xef\\'\\xd5\\xcb\\x16b\\xaf\\x16\\xb7\\x1c\\xd9`Tg\\xa0\\xa0\\x02\"C\\xc8\\xa1\\x9e\\xf0\\xbc\\x9d\\xbab\\x86\\xc6\\xd9\\xa7}\\xeb\\xe4\\xda\\xf3\\x04\\xa9cT\\x1d\\x8a\\xcc\\xb3\\x04f\\x82\\'\\x81g:*\\x9d\\x95\\xb6\\x7f.\\x1b\\xf8\\xb8\\xe5H\\xa5Y\\xe4\\xe9\\xd0\\xc0\\xc6\\xc3\"\\x87\\xbc\\xc2\\x12\\xad]Na#c \\n\\xd7\\xb2\\x8a\\x1c%\\xd7en\\x97\\xce`\\xa7\\x8a\\xbd\\xeb\\x99\\x9f3\\xd2\\n\\xf8\\xab7\\x0e\\x1ax\\x02\\xdd\\xc0D\\xe7\\xda\\xc8\\xd9\\x1b\\xd7%\\x08\\x7f\\xa6\\xc9\\x88\\xc4\\x8d\\xe8d\\x8eKy\\xfb\\xdf\\xfbJ\\xd1\\xc6\\xf6S\\xc5z1I\\x8c\\x11:\\xdf{[\\x11\\x9dIg{\\x87s\\xc7wi\\x1c\\xbdb}F\\xe2\\x8f\\x7f\\x984\\xdb\\x8a\\x8c~\\xe92\\xf8\\x1c\\xc9\\xc5\\xf3\\xce$\\xc3\\xdd8S\\xff\\xc0\\xb1[\\xbb&e\\xd3\\x92\\x00\\x8c\\x06\\xd3+\\x81\\x1cZ\\x02', timestamp=1234, vaccine='a vaccine', version='1')"
    assert str(eval(representation)) == \
"""-----------------------
  Transaction: VaccineTransaction
  Senderpubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Signature: 78fda64d7c858986bd22a8d6fca3b4cd7b59edf4cfb9c902093ce694cc4725b2892d28e8f37944efb0eba18d1359205a495e85ef27d5cb1662af16b71cd9605467a0a0022243c8a19ef0bc9dba6286c6d9a77debe4daf304a963541d8accb30466822781673a2a9d95b67f2e1bf8b8e548a559e4e9d0c0c6c32287bcc212ad5d4e612363200ad7b28a1c25d7656e97ce60a78abdeb999f33d20af8ab370e1a7802ddc044e7dac8d91bd725087fa6c988c48de8648e4b79fbdffb4ad1c6f653c57a31498c113adf7b5b119d49677b8773c777691cbd627d46e28f7f9834db8a8c7ee932f81cc9c5f3ce24c3dd3853ffc0b15bbb2665d392008c06d32b811c5a02
  Timestamp: 1234
  Vaccine: a vaccine
  Version: 1
-----------------------"""

def test_transaction_signature_verification(signed_tx):
    assert signed_tx.validate() == True
    signed_tx.vaccine = 'another vaccine' # tamper with the transaction
    assert signed_tx.validate() == False, "signature check should return False on tampered transaction"