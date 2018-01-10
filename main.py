"""This file is for playing around. Feel free to alter it."""

from blockchain.block import *
from blockchain.transaction import *
from Crypto.PublicKey import RSA


if __name__ == "__main__":
    with open("tests" + os.sep + "testkey_pub.bin", "rb") as public_key, open("tests" + os.sep + "testkey_priv.bin", "rb") as private_key:
        PUBLIC_KEY = RSA.import_key(public_key.read())
        PRIVATE_KEY = RSA.import_key(private_key.read())
    genesis = create_initial_block()
    new_transaction = VaccineTransaction('a vaccine', PUBLIC_KEY).sign(PRIVATE_KEY)
    genesis.add_transaction(new_transaction)
    new_transaction = PermissionTransaction(Permission.doctor,PUBLIC_KEY).sign(PRIVATE_KEY)
    genesis.add_transaction(new_transaction)
    genesis.update_hash()
    # print(repr(asd))
    genesis.persist()
    blockchain_folder = "blockchain"
    persistence_folder = os.path.join(blockchain_folder,
                                      CONFIG["persistance_folder"])
    with open(os.path.join(persistence_folder, '0'), 'r') as file:
        recreated_block = Block(file.read())

    print(genesis)
    print(recreated_block)
