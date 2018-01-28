"""This module handles all network requests from client module.

Since we are not establishing a Peer-To-Peer network in this prototype, we
implement the necessary network operations via REST-Api calls. All REST calls
are bundled in this file in order to provide easy exchangeability.
"""

from abc import ABCMeta
import requests
from ..config import CONFIG


class Network(ABCMeta):
    """Facade for network operations."""

    @staticmethod
    def send_block(node, block_data):
        """Send a block to the specified node."""
        route = node + CONFIG["ROUTES"]["new_block"]
        requests.post(route, data=block_data, timeout=5)

    @staticmethod
    def request_latest_block(node):
        """Ask another node for current chain status."""
        route = node + CONFIG["ROUTES"]["latest_block"]
        return requests.get(route)

    @staticmethod
    def broadcast_new_transaction(node, transaction):
        """Broadcast a transaction to neighbours."""
        route = node + CONFIG["ROUTES"]["new_transaction"]
        requests.post(route, data=transaction, timeout=5)
