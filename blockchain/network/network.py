"""This module handles all network requests from client module.

We implement the necessary network operations via REST-Api calls. All REST calls
are bundled in this file in order to provide easy exchangeability.

In general each method takes 2 arguments. First argument will be the base URI of the destination (e.g. 'http://127.0.0.1:9000').
The second argument is the data that neeeds to be send. It will be the sting representation of a object (`repr()`).
"""
import socket
from abc import ABCMeta
import requests
from ..config import CONFIG
import logging
import time
import random

logger = logging.getLogger("network")
ARTIFICIAL_LATENCY_ENABLED = CONFIG["artificial_latency_enabled"]


class Network(ABCMeta):
    """Facade for network operations."""

    @staticmethod
    def send_block(node, block_data):
        """Send a block to the specified node.

        :param node: String of complete base URI. E.g. 'http://127.0.0.1:9000'
        :param block_data: String representation of a block (`repr()`)
        """
        route = node + CONFIG["ROUTES"]["new_block"]
        simulate_latency()
        try:
            r = requests.post(route, data=block_data, timeout=5)
        except requests.exceptions.ReadTimeout as r:
            logger.debug("Got a ReadTimeout while sending block to {}: {}".format(route, r))
            return False
        except requests.exceptions.ConnectionError as r:
            logger.debug("Got Exception while connecting to {}: {}".format(route, r))
            return  False
        return r.ok

    @staticmethod
    def broadcast_new_transaction(node, transaction):
        """Send a transaction to a neighbour.

        :param node: String of complete base URI. E.g. 'http://127.0.0.1:9000'
        :param transaction: String representation of a transaction (`repr()`)
        """
        route = node + CONFIG["ROUTES"]["new_transaction"]
        try:
            requests.post(route, data=transaction)
        except requests.exceptions.ReadTimeout as r:
            logger.debug("Got a ReadTimeout while sending transaction to {}: {}".format(route, r))
        except requests.exceptions.ConnectionError as r:
            # This Exception will mostly occur when trying to connect to a non admission node
            logger.debug("Got Exception while connecting to {}: {}".format(route, r))

    @staticmethod
    def send_judgement(node, judgement):
        """Send a judgement to a neighbour.

        :param node: String of complete base URI. E.g. 'http://127.0.0.1:9000'
        :param judgement: String representation of a judgement (`repr()`)
        """
        route = node + CONFIG["ROUTES"]["new_judgement"]
        try:
            requests.post(route, data=judgement)
        except requests.exceptions.ReadTimeout as r:
            logger.debug("Got a ReadTimeout while sending judgegment to {}: {}".format(route, r))
        except requests.exceptions.ConnectionError as r:
            logger.debug("Got Exception while connecting to {}: {}".format(route, r))

    @staticmethod
    def send_sync_request(node, block):
        """Send a request for sync to a neighbour.

        :param node: String of complete base URI. E.g. 'http://127.0.0.1:9000'
        :param block: String representation of a block (`repr()`)
        """
        route = node + CONFIG["ROUTES"]["sync_request"]
        hostname = socket.gethostname()
        data = [hostname, block]
        try:
            r = requests.post(route, data=repr(data))
        except requests.exceptions.ReadTimeout as r:
            logger.debug("Got a ReadTimeout while sending sync request to {}: {}".format(route, r))
            return False
        except requests.exceptions.ConnectionError as r:
            logger.debug("Got Exception while connecting to {}: {}".format(route, r))
            return False
        return r.ok

def simulate_latency():
    """Wait for a short period to simulate network latency.

    Before making a request, the network module will sleep a random amount of
    time. Waiting can be disabled in the config file. Furthermore, the
    configuration of the waiting is located there as well.
    """
    if ARTIFICIAL_LATENCY_ENABLED:
        sleep_interval = CONFIG["sleep_interval"]
        sleep_time = random.uniform(sleep_interval[0], sleep_interval[1])
        logger.debug("Set random sleep time to {} seconds."
                     .format(round(sleep_time, 3)))
        time.sleep(sleep_time)
