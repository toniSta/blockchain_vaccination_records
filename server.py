from flask import Flask, request
import os

from blockchain.full_client import FullClient

app = Flask(__name__)
full_client = FullClient()


@app.route('/new_block', methods=['POST'])
def new_block():
    full_client.received_new_block(request.data.decode("utf-8") )
    return "success"


@app.route('/request_block/index/<index>', methods=['GET'])
def send_block_by_id(index):
    block = full_client.chain.find_block_by_index(int(index))
    return repr(block)


@app.route('/request_block/hash/<hash>', methods=['GET'])
def send_block_by_hash(hash):
    block = full_client.chain.find_block_by_hash(hash)
    return repr(block)


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    new_transaction = request.data
    full_client.handle_new_transaction(new_transaction, False)
    return "success"


@app.route('/latest_block', methods=['GET'])
def latest_block():
    block = full_client.chain.last_block()
    return repr(block)


if __name__ == '__main__':
    port = 9000
    if os.getenv('SERVER_PORT'):
        port = int(os.getenv('SERVER_PORT'))
    app.run(host='0.0.0.0', port=port)
