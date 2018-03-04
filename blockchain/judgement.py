import logging
from time import time

from blockchain.config import CONFIG
import blockchain.helper.key_utils as key_utils
import blockchain.helper.cryptography as crypto
logger = logging.getLogger("judgement")


class Judgement(object):
    """This class implements the judgement functionality."""

    def __init__(self, hash_of_judged_block, accept_block, sender_pubkey, signature=None, timestamp=None, version=None):
        if type(sender_pubkey).__name__ == "RsaKey":
            sender_pubkey = key_utils.rsa_to_bytes(sender_pubkey)
        elif type(sender_pubkey).__name__ == "str":
            sender_pubkey = key_utils.hex_to_bytes(sender_pubkey)

        self.hash_of_judged_block = hash_of_judged_block
        self.accept_block = accept_block
        self.sender_pubkey = sender_pubkey
        self.signature = signature
        self.timestamp = timestamp or int(time())
        self.version = version or CONFIG["version"]

    def sign(self, private_key):
        """Create a cryptographic signature and add it to the judgement."""
        if self.signature:
            logger.debug("judgement already signed.")
            return
        self.signature = self._create_signature(private_key)
        return self

    def _create_signature(self, private_key):
        message = crypto.get_bytes(self._get_data_for_hashing())
        return crypto.sign(message, private_key)

    def _get_data_for_hashing(self):
        """Return a string representation of the contained data for hashing"""
        return str({
            "judged_block": self.hash_of_judged_block,
            "accept_block": self.accept_block,
            "sender_pubkey": self.sender_pubkey,
            "timestamp": self.timestamp,
            "version": self.version
        })

    def validate(self):
        """Check if the judgement meets the requirements.

        Checks if the signature is valid,
        WONTFIX: Should check if the judge is an admission node
        """
        return self._verify_signature()

    def _verify_signature(self):
        if not self.signature:  # fail if object has no signature attribute
            return False
        message = crypto.get_bytes(self._get_data_for_hashing())
        return crypto.verify(message, self.signature, key_utils.bytes_to_rsa(self.sender_pubkey))

    def __repr__(self):
        """
        This method returns a string representation of the object such that eval() can recreate the object.
        The Class attributes will be ordered
        e.g. Class(attribute1="String", attribute2=3)
        """
        instance_member_list = []
        for item in vars(self).items():
            instance_member_list.append(item)
        instance_member_list.sort(key=lambda tup: tup[0])

        return "{!s}({!s})".format(
            type(self).__name__,
            ", ".join(["{!s}={!r}".format(*item) for item in instance_member_list])
        )

    def __str__(self):
        return ("-----------------------\n"
                "  Judgement\n"
                "  Judged block: {}\n"
                "  Accept block: {}\n"
                "  Public key: {}\n"
                "  Timestamp: {}\n"
                "  Version: {}\n"
                "-----------------------").format(self.hash_of_judged_block,
                                                  self.accept_block,
                                                  self.sender_pubkey,
                                                  self.timestamp,
                                                  self.version)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
