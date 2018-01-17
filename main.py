"""This file is for playing around. Feel free to alter it."""

from blockchain.block import *
from blockchain.chain import Chain
from blockchain.full_client import FullClient
from blockchain.transaction import *
from Crypto.PublicKey import RSA
import requests


if __name__ == "__main__":

    response = requests.get('http://127.0.0.1:9000/latest_block')
    content = response.text

    block = Block(content)


    print("Block index is:" + str(block.index))
    print("Block hash is:" + block.hash)

    with open("tests" + os.sep + "testkey_pub.bin", "rb") as public_key, open("tests" + os.sep + "testkey_priv.bin", "rb") as private_key:
        PUBLIC_KEY = RSA.import_key(public_key.read())
        PRIVATE_KEY = RSA.import_key(private_key.read())
    new_transaction = VaccineTransaction("a vaccine", PUBLIC_KEY).sign(PRIVATE_KEY)
    requests.post('http://127.0.0.1:9000/new_transaction', data=repr(new_transaction))

    full_client = FullClient()
    full_client.synchronize_blockchain()



def blocks():
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
    with open(os.path.join(CONFIG["persistance_folder"], "1"), "r") as file:
        recreated_block = Block(file.read())

    print(chain.find_block_by_index(0))
    print(new_block)
    print(recreated_block)

    # can build new block based on recreated block
    Block(recreated_block.get_block_information())
