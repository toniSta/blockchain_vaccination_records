import logging

CONFIG = {
    "loglevel": logging.DEBUG,
    "version": "0.0.1",
    "persistance_folder": "blockchain/blockchain_files",
    "serializaton": {
        "separator": ",",
        "line_terminator": "\n"
    },
    'block_size': 1024,
}
