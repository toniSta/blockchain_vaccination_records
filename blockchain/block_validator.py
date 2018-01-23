from .config import CONFIG


def validate(block, previous_block):
    if block.index != previous_block.index + 1:
        error = "Wrong index, block index {}, index of last block {}"\
                .format(block.index, previous_block.index)
        return error

    if block.previous_block != previous_block.hash:
        error = "New block does not reference previous one, block hash {},\
                 hash of last block {}"\
                .format(block.hash, previous_block.hash)
        return error

    if block.version != CONFIG["version"]:
        error = "Different versions, block version {}, chain version {}"\
                .format(block.version, CONFIG["version"])
        return error


    return
