from flask import Flask, request
import os
from multiprocessing import Pool

from ..config import CONFIG

app = Flask(__name__)


def handle_received_block(block):
    """ Handle new received block in extra thread for early return."""
    full_client.received_new_block(block)


@app.route(CONFIG["ROUTES"]["new_block"], methods=["POST"])
def _new_block():
    block = request.data.decode("utf-8")
    pool = Pool(processes=1)
    pool.apply_async(handle_received_block, (block,))
    return "success"


@app.route(CONFIG["ROUTES"]["block_by_index"], methods=["GET"])
def _send_block_by_id(index):
    block = full_client.chain.find_block_by_index(int(index))
    return repr(block)


@app.route(CONFIG["ROUTES"]["block_by_hash"], methods=["GET"])
def _send_block_by_hash(hash):
    block = full_client.chain.find_block_by_hash(hash)
    return repr(block)


@app.route(CONFIG["ROUTES"]["new_transaction"], methods=["POST"])
def _new_transaction():
    new_transaction = request.data
    full_client.handle_new_transaction(new_transaction, False)
    return "success"


@app.route(CONFIG["ROUTES"]["latest_block"], methods=["GET"])
def _latest_block():
    block = full_client.chain.last_block()
    return repr(block)


def start_server(client):
    """Start the flask server."""
    global full_client
    full_client = client
    port = CONFIG["default_port"]
    if os.getenv("SERVER_PORT"):
        port = int(os.getenv("SERVER_PORT"))
    app.run(host="0.0.0.0", port=port)
