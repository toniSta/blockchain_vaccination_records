import logging
import blockchain.helper.cryptography as crypto
from Crypto.PublicKey import RSA
from time import time
from enum import Enum

from blockchain.config import CONFIG

# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format='[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger('blockchain')

def hexify(s):
    if s is None:
        return ""
    else:
        return s.hex()

class Permission(Enum):
    patient = "patient"
    admission = "admission"
    doctor = "doctor"


class PermissionTransaction(object):
    def __init__(self, requested_permission, sender_pubkey):
        logger.debug('Creating new permission transaction')
        self.version = CONFIG['version']
        self.timestamp = int(time())
        self.requested_permission = requested_permission
        self.sender_pubkey = sender_pubkey.exportKey("DER")
        self.signature = None

    def __str__(self):
        return ('-----------------------\n'
                '  Transaction: \n'
                '  Permission Request: {}\n'
                '  Sender: {}\n'
                '  Signature: {}\n'
                '  Timestamp: {}\n'
                '-----------------------').format(self.requested_permission,
                        self.sender_pubkey.hex(),
                        hexify(self.signature),
                        self.timestamp)

    def get_transaction_information(self):
        return {
            'version': self.version,
            'timestamp': self.timestamp,
            'requested_permission': self.requested_permission,
            'sender_wallet': self.sender_pubkey,
            'signature': self.signature
        }

    def _get_informations_for_hashing(self):
        return {
            'version': self.version,
            'timestamp': self.timestamp,
            'requested_permission': self.requested_permission.name,
            'sender_wallet': self.sender_pubkey
        }

    def validate(self):
        """
        checks if the transaction fulfills the requirements
        e.g. if enough positive votes were cast for an admission,
        signature matches, etc.
        """
        return self._verify_signature() # TODO check other requirements

    def _verify_signature(self):
        message = crypto.get_bytes(str(self._get_informations_for_hashing()))
        return crypto.verify(message, self.signature, RSA.import_key(self.sender_pubkey))

    def _create_signature(self, private_key):
        message = crypto.get_bytes(str(self._get_informations_for_hashing()))
        return crypto.sign(message, private_key)

    def sign(self, private_key):
        """creates a signature and adds it to the transaction"""
        self.signature = self._create_signature(private_key)

