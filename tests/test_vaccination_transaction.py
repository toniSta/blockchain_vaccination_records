from Crypto.PublicKey import RSA
from blockchain.transaction.vaccination_transaction import VaccinationTransaction

import pytest
import os
import mock
import sys


PUBLIC_KEY = RSA.import_key(open("tests" + os.sep + "testkey_pub.bin", "rb").read())
PRIVATE_KEY = RSA.import_key(open("tests" + os.sep + "testkey_priv.bin", "rb").read())

@pytest.fixture()
def tx():
    tx = VaccinationTransaction(PUBLIC_KEY, PUBLIC_KEY, 'polio', timestamp=1234, version='1')
    yield tx

@pytest.fixture()
def signed_tx():
    tx = VaccinationTransaction(PUBLIC_KEY, PUBLIC_KEY, 'polio', timestamp=1234, version='1')
    with mock.patch.object(sys.stdin, 'read', lambda x: 'y'):
        tx.sign(PRIVATE_KEY, PRIVATE_KEY)
    yield tx

@pytest.fixture()
def declined_tx():
    tx = VaccinationTransaction(PUBLIC_KEY, PUBLIC_KEY, 'polio', timestamp=1234, version='1')
    with mock.patch.object(sys.stdin, 'read', lambda x: 'n'):
        tx.sign(PRIVATE_KEY, PRIVATE_KEY)
    yield tx

def test_representation(signed_tx):
    representation = repr(signed_tx)
    assert representation == "VaccinationTransaction(doctor_pub_key=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', doctor_signature=b'\\x04\\x92\\x90a\\xb9$\\xd4S\\xed\\xea\\\\\\xa6)\\xc8\\xe6b\\xf5xA\\xe2(\\xdf\\x0e6\\xfc\\xef(\\x84\\t\\xa5\\x13\\x84\\xe2\\xbdx\\xa2\\xa2F4\\xb1d1gIC\\x8fq\\xc7\\xb2S1\\x95)\\xe1\\xf9\\xa9\\xbe\\xa3\\xd7~h \\xc4<\\xf0\\xd7R\\xff{\\xe7\\xd4\\xa9\\xc04\\xf3x\\xeax\\xcd\\xf6j\\xd5\\x94\\xe4\\xe2\\xc7D\\x90\\xddI3\\x1f\\x1cV\\xa47\\xd3\\x013\\xa5AO\\xa66\\x8d,\\x18\\x8bj8\\xcbo\\xca!\\xf9\\xad\\x0bM\\xcc&\\x00\\xec\\xf40&m\\xc5\\xa4B\\x91R\\xc8\\x167\\xf5W\\xfe\\xb1\\xb03\\x96\\xb0\\xfe\\x8e4\\x0bi%\\xeb\\x96\\xaf\\xbc\\xca\\x12n\\x7f\\xc0\\x0f\\xbb\\xcf@\\x02\\xae\\xe8\\xb0\\x9e\\x97\\xa4\\x1a\\xe7a7J\\xd1\\xf4/\\x8c]\\x02\\xf2\\x15\\xe9\\x847\\x19KE\\xc0\\xd8\\xc0\\xb0\\xb8s\\xf5l\\xfa\\x95\\xc4\\xb4\\x1e\\xa0m\\x12\\xafeArQ,\\xc4\\x06\\xe8\\x95\\xb8<\\xed\\x0b\\xaf\\x83\\x1ab\\xebvZjB3\\xb6\\xd4l|\\xea\\x10\\xcc\\xaf\\xee\\xc5!B\\xac\\x02\\xb3*\\xac\\xd9\\x98.6\\x17\\xd1\\x9dk\\xd8\\x0bo\\x9b', patient_pub_key=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', patient_signature=b\"q{\\x86\\x0e\\xa2t\\xe7\\x92\\xf0\\xb0\\x0cQ\\x11\\x98Hb?\\x8f\\x1aO<\\x1cd\\xf9\\x85\\xe12%\\x13\\x94z\\xdd\\xb86\\x99\\xaeV\\xf9M\\xc1\\xe1\\xdd\\xdd\\xf0Wv\\x965;\\xfb\\xf4\\xfc\\xed\\xfe\\n\\t\\xfc\\xa5\\x05C\\x06\\x1c\\x87m\\xd8\\x1b\\xdd\\xbc\\x08Lo\\x1c\\x140\\x08|\\xa2@m'\\xce\\x99\\xe0\\x1a\\xb1\\xc9\\x9e\\xbb\\xe5/o\\xbfnA[&4\\x1e\\xb7\\xb1\\x1e\\xd0\\xe8\\x9cy\\x9c\\xe1w\\xa7\\xb3K\\\\\\x81\\xd8\\x1aM\\x1e\\x19-\\xfa\\x803\\xe7\\xfd\\xa9\\x00Q=W{\\xad6\\x0c\\xad\\xad\\x81^,\\xad0\\x1a\\xed\\x9b\\x8ay\\x1d\\xb1V\\xe3\\x1c\\x15\\xe1\\x95V\\x1b\\x14\\xe0\\xdb\\xa1\\xa4\\x8d,\\xbb\\xde\\xfa\\x9az\\x04\\x87\\xb1\\x8a\\xaa\\x82+\\xc9\\x8bf\\x83\\xcc\\xfe\\x95\\xea+\\x87\\xc6\\xc46_\\x82\\xa3m\\xb7\\xf6\\x85Zpc\\xb3\\xb1\\xe7\\xa4<\\xefb\\xba\\xb6\\xadH\\xa6H\\xdd\\x91E\\x85\\x13\\x11@n\\xb3\\xde\\x81\\xe2F\\x1c\\t\\xfdA\\xf7,\\x1e\\xdd\\xad\\xdc\\x91\\xb3>\\x91j\\x0e\\x91\\xd6\\xa2;\\x07X\\x1f\\xdbD\\x1f\\x16\\xd9\\x88\\xf6\\xb2\\xc9q\", timestamp=1234, vaccine='polio', version='1')"
    assert str(eval(representation)) == \
"""-----------------------
  Transaction: VaccinationTransaction
  Doctor_Pub_Key: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Doctor_Signature: 04929061b924d453edea5ca629c8e662f57841e228df0e36fcef288409a51384e2bd78a2a24634b164316749438f71c7b253319529e1f9a9bea3d77e6820c43cf0d752ff7be7d4a9c034f378ea78cdf66ad594e4e2c74490dd49331f1c56a437d30133a5414fa6368d2c188b6a38cb6fca21f9ad0b4dcc2600ecf430266dc5a4429152c81637f557feb1b03396b0fe8e340b6925eb96afbcca126e7fc00fbbcf4002aee8b09e97a41ae761374ad1f42f8c5d02f215e98437194b45c0d8c0b0b873f56cfa95c4b41ea06d12af654172512cc406e895b83ced0baf831a62eb765a6a4233b6d46c7cea10ccafeec52142ac02b32aacd9982e3617d19d6bd80b6f9b
  Patient_Pub_Key: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Patient_Signature: 717b860ea274e792f0b00c51119848623f8f1a4f3c1c64f985e1322513947addb83699ae56f94dc1e1ddddf0577696353bfbf4fcedfe0a09fca50543061c876dd81bddbc084c6f1c1430087ca2406d27ce99e01ab1c99ebbe52f6fbf6e415b26341eb7b11ed0e89c799ce177a7b34b5c81d81a4d1e192dfa8033e7fda900513d577bad360cadad815e2cad301aed9b8a791db156e31c15e195561b14e0dba1a48d2cbbdefa9a7a0487b18aaa822bc98b6683ccfe95ea2b87c6c4365f82a36db7f6855a7063b3b1e7a43cef62bab6ad48a648dd9145851311406eb3de81e2461c09fd41f72c1eddaddc91b33e916a0e91d6a23b07581fdb441f16d988f6b2c971
  Timestamp: 1234
  Vaccine: polio
  Version: 1
-----------------------"""

def test_transaction_signature_verification(signed_tx):
    current_admissions = set()  # mock empty chain with no admissions
    doctors = set()  # mock registered doctors
    doctors.add(signed_tx.doctor_pub_key)
    vaccines = set()  # mock registered vaccine
    vaccines.add('polio')
    assert signed_tx.validate(current_admissions, doctors, vaccines) == True
    signed_tx.vaccine = 'another vaccine' # tamper with the transaction
    assert signed_tx.validate(current_admissions, doctors, vaccines) == False, "signature check should return False on tampered transaction"

def test_transaction_patient_acceptance(declined_tx):
    assert declined_tx.patient_signature is None
