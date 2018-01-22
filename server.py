import logging
from flask import Flask, request
import os

from blockchain.full_client import FullClient
from blockchain.config import CONFIG

app = Flask(__name__)
full_client = FullClient()


@app.route(CONFIG["ROUTES"]["new_block"], methods=["POST"])
def _new_block():
    full_client.received_new_block(request.data.decode("utf-8"))
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format="[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.WARNING)

    port = 9000
    if os.getenv("SERVER_PORT"):
        port = int(os.getenv("SERVER_PORT"))
    app.run(host="0.0.0.0", port=port)
