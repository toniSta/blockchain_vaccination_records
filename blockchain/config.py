import logging

CONFIG = {
    'loglevel': logging.DEBUG,
    'version': '0.0.1',
    'persistance_folder': 'blockchain_files',
    'serializaton': {
        'separator': ',',
        'line_terminator': '\n'
    },
    'BLOCK_SIZE': 1024,
}
