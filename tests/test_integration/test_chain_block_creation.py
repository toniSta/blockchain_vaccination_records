from blockchain.block import *
from blockchain.chain import Chain
from blockchain.transaction import *
from Crypto.PublicKey import RSA


def test_chain_and_block_creation():
    with open("tests" + os.sep + "testkey_pub.bin", "rb") as public_key, open("tests" + os.sep + "testkey_priv.bin", "rb") as private_key:
        PUBLIC_KEY = RSA.import_key(public_key.read())
        PRIVATE_KEY = RSA.import_key(private_key.read())

    # Create chain, append genesis block
    chain = Chain(load_persisted=False)
    genesis = create_initial_block(PUBLIC_KEY, PRIVATE_KEY)
    chain.add_block(genesis)

    assert chain.size() == 1

    # new Block with transactions
    new_block = Block(chain.last_block().get_block_information(), PUBLIC_KEY)
    new_transaction = VaccineTransaction("a vaccine", PUBLIC_KEY).sign(PRIVATE_KEY)
    new_block.add_transaction(new_transaction)
    new_transaction = PermissionTransaction(Permission.doctor, PUBLIC_KEY).sign(PRIVATE_KEY)
    new_block.add_transaction(new_transaction)

    new_block.sign(PRIVATE_KEY)
    new_block.update_hash()
    new_block.persist()

    # read file from disk
    with open(os.path.join(CONFIG["persistance_folder"], "1"), "r") as file:
        recreated_block = Block(file.read())

    assert repr(new_block) == repr(recreated_block), \
        "Recreated block must have same representation as initial one."
    # can build new block based on recreated block
    Block(recreated_block.get_block_information(), PUBLIC_KEY)
