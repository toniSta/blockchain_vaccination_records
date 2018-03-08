from blockchain.config import CONFIG

def setup_test_config():
    CONFIG.persistance_folder = "tests/blockchain_files"
    CONFIG.key_folder = "tests/keys"
