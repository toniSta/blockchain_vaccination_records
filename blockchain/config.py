import logging

CONFIG = {
    "loglevel": logging.DEBUG,
    "version": "0.0.1",
    "persistance_folder": "blockchain/blockchain_files",
    "serializaton": {
        "separator": ",",
        "line_terminator": "\n"
    },
    "block_size": 1024,
    # Create a block every n seconds. N has to be at least 2
    "block_time": 5,
    "key_folder": "blockchain/keys",
    "key_file_names": ["public_key.bin", "private_key.bin"]
}
