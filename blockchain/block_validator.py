from .config import CONFIG
import logging

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

    return True
