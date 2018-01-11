from flask import Flask, request
import os

from blockchain.node import Node

app = Flask(__name__)
node = Node()


@app.route('/new_block', methods=['POST'])
def new_block():
    return "Hello World!"


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    new_transaction = request.data
    node.handle_new_transaction(new_transaction)
    return "success"


@app.route('/latest_block', methods=['GET'])
def latest_block():
    block = node.chain.last_block()
    return repr(block)


if __name__ == '__main__':
    port = 9000
    if os.getenv('PORT'):
        port = int(os.getenv('PORT'))
    app.run(port=port)
