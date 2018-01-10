"""This file is for playing around. Feel free to alter it."""

from blockchain.block import *
from blockchain.chain import Chain
from blockchain.transaction import *
from Crypto.PublicKey import RSA


if __name__ == "__main__":
    with open("tests" + os.sep + "testkey_pub.bin", "rb") as public_key, open("tests" + os.sep + "testkey_priv.bin", "rb") as private_key:
        PUBLIC_KEY = RSA.import_key(public_key.read())
        PRIVATE_KEY = RSA.import_key(private_key.read())

    # Create chain, already contains empty genesis
    chain = Chain()

    # new Block with transactions
    new_block = Block(chain.last_block().get_block_information())
    new_transaction = VaccineTransaction("a vaccine", PUBLIC_KEY).sign(PRIVATE_KEY)
    new_block.add_transaction(new_transaction)
    new_transaction = PermissionTransaction(Permission.doctor, PUBLIC_KEY).sign(PRIVATE_KEY)
    new_block.add_transaction(new_transaction)

    new_block.update_hash()
    new_block.persist()

    # read file from disk
    blockchain_folder = "blockchain"
    persistence_folder = os.path.join(blockchain_folder,
                                      CONFIG["persistance_folder"])
    with open(os.path.join(persistence_folder, "1"), "r") as file:
        recreated_block = Block(file.read())

    print(chain.find_block_by_index(0))
    print(new_block)
    print(recreated_block)

    # can build new block based on recreated block
    Block(recreated_block.get_block_information())
