from flask import Flask, request, jsonify
import os

from blockchain.node import Node

app = Flask(__name__)
node = Node()


@app.route('/new_block', methods=['POST'])
def new_block():
    import pdb; pdb.set_trace()
    return "Hello World!"


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    import pdb; pdb.set_trace()
    return "Hello World!"


@app.route('/latest_block', methods=['GET'])
def latest_block():
    block = node.chain.last_block()
    response = {
        "index": block.index,
        "hash": block.hash
    }
    return jsonify(response)


# requests.get('https://api.github.com/events')


if __name__ == '__main__':
    port = 9000
    if os.getenv('PORT'):
        port = int(os.getenv('PORT'))
    app.run(port=port)
