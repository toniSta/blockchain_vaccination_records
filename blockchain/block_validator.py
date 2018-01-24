from Crypto.PublicKey import RSA
import logging
from time import time

import blockchain.helper.cryptography as crypto
from .config import CONFIG

logger = logging.getLogger("block-validator")


def validate(block, previous_block):
    if block.index != previous_block.index + 1:
        logger.info("Wrong index, block index {}, index of last block {}"
                    .format(block.index, previous_block.index))
        return False

    if block.previous_block != previous_block.hash:
        logger.info(("New block does not reference previous one, block hash"
                     " {}, hash of last block {}")
                    .format(block.hash, previous_block.hash))
        return False

    if block.version != CONFIG["version"]:
        logger.info("Different versions, block version {}, chain version {}"
                    .format(block.version, CONFIG["version"]))
        return False

    if block.timestamp > int(time()):
        # TODO deviation in the past ??
        logger.info("Timestamp of the new block is in the future")
        return False

    # if block.public_key not in admission nodes?

    relevant_block_content = str.encode(block.get_content_for_signing())
    signature = bytes.fromhex(block.signature)
    public_key = RSA.importKey(bytes.fromhex(block.public_key))
    # import pdb; pdb.set_trace()
    valid = crypto.verify(relevant_block_content, signature, public_key)
    if not valid:
        logger.info("Signature is not valid, block must be altered")
        return False
    return True
