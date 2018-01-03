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
    assert representation == "VaccinationTransaction(doctorPubKey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', doctorSignature=b'\\xa7\\xb7sP\\x01\\xb0\\xd2\\x1e\\xee\\x19`\\x9a\\xf7\\xfa\\xb9j\\x145\\xd5Vr\\xa9\"\\xea#\\xcak\\x16I#\\x80k\\x98\\xbb\\xc8G\\x89\\xcb\\x87q\\xc0\\x8b[\\xb4RVn\\xd3\\xb0\\xdd\\xca%\\xce[+\\x83G\\x17\\xb9\\xff\\x8a\\xd5`\\x15g\\x01\\x08]\\x0b\\x93\\x14\\xb2]8\\xc5A\\x81\\xf8\\xef\\xa8\\xfc\\xd19a1R\\xa1\\xf3gH\\xfcg\\x80_.(`\\xd1\\xf9\\x83!\\x85\\x07\\x8f\\xd0\\x15\\xb3\\x1a\\xc8\\xa6\\xa2\\x9d|\\xe2o1\\x89hk\\x92\\x8a\\x03Xu\\xf2\\xff<=.\\xda\\xd36\\xf4G\\xd1\\x92`\\xc7\\xa2,\\xe6\\x91(\\x9e\\xc7\\xbb/\\x96I\\xa7\\xcac\\x00\\xfaJ\\x83\\xcd\\xebw\\xb4g\\x13T\\xf1\\x88\\xb6\\x01\\x8e\\x81\\x87\\xc1\\x82N\\xab\\x9b\\'\\xd9%-p\\x83\\xa4x\\xd4K\\x0c\\xee\\xd7{\\xe9\\x17\"\\xfd\\x9e\\x07\\x88G\\xe5\\xeb\\x11\\xc3C\\x06\\x06e\\xa0\\x88\\xb1\\n1\\x8f2F\\x0f\\xbcp\\x93\\x1c\\xa5\\xc2\\xdbt\\xb6\\x91\\xf5sw\\xe1G\\xca\\xddK\\x96x\\x82\\x0c\\x92\\x8d\\xde\\xc2\\xd4\\x89;c\\x9a\\x98+\\xa8\\xbe\\xef\\x89?\\xed\\xd2\\xf3\\x82', patientPubKey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', patientSignature=b'{\\xcd^\\x7f1<\\xcd\\xdc\\x11Q\\x9c\\xb7\\x10Q\\x06\\xf6r\\xe4\\x82\\x91\\xdfo<6\\xd7s0u%\\xb0d\\xdd%\\xfb\\x98{8\\xbd\\x99\\xea\\x0b\\r:\\x1c\\xafGT\\xb4@\\xb2\\xaa\\xde\\x92\\xe9\\xed\\x01t\\xa7\\xc3\\x89tY\\xc9!x\"8\\xd5\\x91aw\\x0c\\xcb(\\x7f;w\\x99\\x13EE\\xd8I:\\x9c\\xea^\\xb6\\x93#\\xe0*\\xbd \\x99L\\xec\\xdd \\x831\\xf4C?\\xcec\\xeb\\xa6\\xd9M\\xce\\xc9N\\x03\\xe9\\xbe\\x89{y.\\xc4\\xa7\\xcc\\xc3\\xbe]\\x1f\\xd2uFj\\xcc\\x85}?y\\xbb\\x05\\xa6}\\xb7\\x01\\xbc\\xcf\\xd9\\xc3=4\\xf9\\xd7bA\\xb8\\xabO\\x9b\\xbb5\\xe6\\x8bG\\x0e26\\x19\\xce\\xde$\\x03\\x84\\xd6}z\\xe8\\xdbY\\xa7\\x8bX\\xd6J\\x9d\\xa4v5K\\xa1X\\x07i\\x85\\xee\\x0fI\\xd3\\xba^9\\x96E\\x8a\\x00\\xac\\x97\\x01_\\x11v\\x07\\x9b<z\\xbb\\xea\\x18\\xca\\x9f\\x05\\x15\\xdc\\x06\\xdf\\xd1\\xf9\\xf9nt\\xc2\\xa6\\x0e\\xeaA\\x92\\xb6^\\xad\\xad\\x12A\\x06\\x7f\\xf5\\xc8\\xae\\xf1\\x08\\x8f\\r\\xd1?\\xb8:|\\x17\\x16\\xef', timestamp=1234, vaccine='polio', version='1')"
    assert str(eval(representation)) == \
"""-----------------------
  Transaction: VaccinationTransaction
  Doctorpubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Doctorsignature: a7b7735001b0d21eee19609af7fab96a1435d55672a922ea23ca6b164923806b98bbc84789cb8771c08b5bb452566ed3b0ddca25ce5b2b834717b9ff8ad560156701085d0b9314b25d38c54181f8efa8fcd139613152a1f36748fc67805f2e2860d1f9832185078fd015b31ac8a6a29d7ce26f3189686b928a035875f2ff3c3d2edad336f447d19260c7a22ce691289ec7bb2f9649a7ca6300fa4a83cdeb77b4671354f188b6018e8187c1824eab9b27d9252d7083a478d44b0ceed77be91722fd9e078847e5eb11c343060665a088b10a318f32460fbc70931ca5c2db74b691f57377e147cadd4b9678820c928ddec2d4893b639a982ba8beef893fedd2f382
  Patientpubkey: 30820122300d06092a864886f70d01010105000382010f003082010a0282010100ae250cf96ced56054a369a7ca4c9ba87d85f2b0b54d398104d9cc397c48a4539b6370de493504eb726c89389a8964af3d9395aeb7cf83f3bb2f74669afa493b850f18d393eb72377eb0409582bbb358192c85dbf5389ad2f651236a6f88136d1ad61ade140b0eb01bb94c6c1ce15451e9b8dec8aa3186ba02b449c071603f9e114e988c229074efab7d61db36d90203441c253021f3783634452e7fe32c480b37de6aff49cd41b9f591060951f2a5eab9c5364c929ebf6e4cf7217795ae160e2611d395ea5e5d2db9c557479b63c004afd544551af8bfb908e8bac4694c683a0e8f756136c636b5bb39db1c172fe9432be3ee630ff460add11fed2c4506aae9b0203010001
  Patientsignature: 7bcd5e7f313ccddc11519cb7105106f672e48291df6f3c36d773307525b064dd25fb987b38bd99ea0b0d3a1caf4754b440b2aade92e9ed0174a7c3897459c921782238d59161770ccb287f3b7799134545d8493a9cea5eb69323e02abd20994cecdd208331f4433fce63eba6d94dcec94e03e9be897b792ec4a7ccc3be5d1fd275466acc857d3f79bb05a67db701bccfd9c33d34f9d76241b8ab4f9bbb35e68b470e323619cede240384d67d7ae8db59a78b58d64a9da476354ba158076985ee0f49d3ba5e3996458a00ac97015f1176079b3c7abbea18ca9f0515dc06dfd1f9f96e74c2a60eea4192b65eadad1241067ff5c8aef1088f0dd13fb83a7c1716ef
  Timestamp: 1234
  Vaccine: polio
  Version: 1
-----------------------"""

def test_transaction_signature_verification(signed_tx):
    assert signed_tx.validate() == True
    signed_tx.vaccine = 'another vaccine' # tamper with the transaction
    assert signed_tx.validate() == False, "signature check should return False on tampered transaction"

def test_transaction_patient_acceptance(declined_tx):
    assert declined_tx.patientSignature is None