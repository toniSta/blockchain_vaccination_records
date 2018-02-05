"""This module handles all network requests from client module.

Since we are not establishing a Peer-To-Peer network in this prototype, we
implement the necessary network operations via REST-Api calls. All REST calls
are bundled in this file in order to provide easy exchangeability.
"""

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
        """Send a block to the specified node."""
        route = node + CONFIG["ROUTES"]["new_block"]
        simulate_latency()
        try:
            requests.post(route, data=block_data, timeout=5)
        except requests.exceptions.ReadTimeout as r:
            logger.debug("Got a ReadTimeout while sending block to {}: {}".format(route, r))
        except requests.exceptions.ConnectionError as r:
            logger.debug("Got Exception while connecting to {}: {}".format(route, r))

    @staticmethod
    def request_latest_block(node):
        """Ask another node for current chain status."""
        route = node + CONFIG["ROUTES"]["latest_block"]
        return requests.get(route)

    @staticmethod
    def broadcast_new_transaction(node, transaction):
        """Broadcast a transaction to neighbours."""
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
        route = node + CONFIG["ROUTES"]["new_judgement"]
        try:
            requests.post(route, data=judgement)
        except requests.exceptions.ReadTimeout as r:
            logger.debug("Got a ReadTimeout while sending judgegment to {}: {}".format(route, r))
        except requests.exceptions.ConnectionError as r:
            logger.debug("Got Exception while connecting to {}: {}".format(route, r))


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
