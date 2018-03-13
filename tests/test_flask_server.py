from blockchain.network import server
from blockchain.config import CONFIG
from tests.config_fixture import setup_test_config
import mock


setup_test_config()


def setup_module(module):
    server.app.config['TESTING'] = True
    module.client = server.app.test_client()
    server.full_client = mock.Mock()
    module.routes_to_test = CONFIG.ROUTES

    # ROUTES = {
    #     "new_block": "/new_block",
    #     "block_by_hash": "/request_block/hash/<hash>",
    #     "new_transaction": "/new_transaction",
    #     "new_judgement": "/new_judgement",
    #     "sync_request": "/sync_request"
    # }


def test_new_block():
    response = client.post(routes_to_test['new_block'])
    assert response.status_code == 200


def test_block_by_hash():
    response = client.get('/request_block/hash/123')
    assert response.status_code == 200


def test_new_transaction():
    vaccine_tx = "VaccineTransaction(sender_pubkey=b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\xae%\\x0c\\xf9l\\xedV\\x05J6\\x9a|\\xa4\\xc9\\xba\\x87\\xd8_+\\x0bT\\xd3\\x98\\x10M\\x9c\\xc3\\x97\\xc4\\x8aE9\\xb67\\r\\xe4\\x93PN\\xb7&\\xc8\\x93\\x89\\xa8\\x96J\\xf3\\xd99Z\\xeb|\\xf8?;\\xb2\\xf7Fi\\xaf\\xa4\\x93\\xb8P\\xf1\\x8d9>\\xb7#w\\xeb\\x04\\tX+\\xbb5\\x81\\x92\\xc8]\\xbfS\\x89\\xad/e\\x126\\xa6\\xf8\\x816\\xd1\\xada\\xad\\xe1@\\xb0\\xeb\\x01\\xbb\\x94\\xc6\\xc1\\xce\\x15E\\x1e\\x9b\\x8d\\xec\\x8a\\xa3\\x18k\\xa0+D\\x9c\\x07\\x16\\x03\\xf9\\xe1\\x14\\xe9\\x88\\xc2)\\x07N\\xfa\\xb7\\xd6\\x1d\\xb3m\\x90 4A\\xc2S\\x02\\x1f7\\x83cDR\\xe7\\xfe2\\xc4\\x80\\xb3}\\xe6\\xaf\\xf4\\x9c\\xd4\\x1b\\x9fY\\x10`\\x95\\x1f*^\\xab\\x9cSd\\xc9)\\xeb\\xf6\\xe4\\xcfr\\x17yZ\\xe1`\\xe2a\\x1d9^\\xa5\\xe5\\xd2\\xdb\\x9cUty\\xb6<\\x00J\\xfdTEQ\\xaf\\x8b\\xfb\\x90\\x8e\\x8b\\xacF\\x94\\xc6\\x83\\xa0\\xe8\\xf7V\\x13lck[\\xb3\\x9d\\xb1\\xc1r\\xfe\\x942\\xbe>\\xe60\\xffF\\n\\xdd\\x11\\xfe\\xd2\\xc4Pj\\xae\\x9b\\x02\\x03\\x01\\x00\\x01', signature=b'\\xa6\\xf9?\\x10\\x8a\\xb7vJ\\x18B\\xd6\\xa44m\\x8aip/\\xed\\xc9(\\x13\\x0f\\xae\\x14>l\\xee\\xedR\\x0cE\\xf7\\x98\\x94`\\xd8\\xc0>\\xc7~\\xd5>jQ\\xcd\\xc3,\\xd0\\xc1\\xeb\\xb5\\xc0[8\\xf6v\\xef\\x0b\\xf0W\\x0c\\xee\\x92\\xf4B\\xba\\xc4\\xc0\\xb8g\\xa0\\xca\\xb9\\xec\\xf5\\x7fq\\xa8\\xc9;9\\xd2S\\x8b\\x19\\xa6\\x9a>[\\x08\\xce@sl\\xd6\\xf69\\xf4}OxX\\x19`\\xfdD\\t\\xd1\\xc2\\\\y.\\xda\\x92\\x05\\x1b\\xe2*z\\xcb\\xcdK\\x93\\xd2\\xa7k2=\\xfeX\\xfa\\xbd\\xec\\xdd\\xe3K6\\xd2\\xd9\\xffm\\x9a\\xf1\\xed\\xcf\\x00\\x89\\xc1\\x98\\xd2\\xb6\\xb5b\\xb2\\xc9\\x9cL\\x1a-.2\\xf3J\\xfa\\xa4\\x89\\x8a\\x95\\xf9A\\xf9uq\\\\\\xe5jS\\xbf\\xa5A\\x03\\x06 \\xdf\\x9f\\xad\\xdc\\x06\\x96\\r\\x8a\\xa1\\x8f\\xa8\\x93\\xb8rD\\x1f\\x00\\xf1\\xa4\\x02\\xd5\\xfe9GL\\xb8\\x8d\\xe4\"\\xcb\\xe69\\x9e4\\x96}\\xf5\\x84\\x824hx\\xc4\\xfavZ\\xe9\\x9f\\x92\\xb0$\\xf4\\xc2\\x05I\\xcd\\xb9\\xb5$\\x1dW\\ns\\xd4v\\x9e;\\x8eW\\xd3\\xbc\\xeb', timestamp=1234, vaccine='a vaccine', version='1')"
    response = client.post(routes_to_test['new_transaction'], data=vaccine_tx)
    assert response.status_code == 200


def test_new_judgement():
    response = client.post(routes_to_test['new_judgement'])
    assert response.status_code == 200


def test_sync_request():
    response = client.post(routes_to_test['sync_request'], data=repr(["host", "asd"]))
    assert response.status_code == 200


@mock.patch('threading.Thread', autospec=True)
def test_start_server(mock1, monkeypatch):
    monkeypatch.setenv('SERVER_PORT', 0)
    monkeypatch.setenv('REGISTER_AS_ADMISSION', 1)
    assert server.start_server(mock.Mock()) is None
