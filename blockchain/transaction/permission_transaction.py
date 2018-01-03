import logging
import blockchain.helper.cryptography as crypto
from Crypto.PublicKey import RSA
from enum import Enum
from blockchain.transaction.transaction import TransactionBase


# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format='[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger('blockchain')


class Permission(Enum):
    patient = "patient"
    doctor = "doctor"
    admission = "admission"

    def __repr__(self):  # overriding to allow recreation with eval()
        return self.__str__()


class PermissionTransaction(TransactionBase):

    def __init__(self, requested_permission, sender_pubkey, signature=None, **kwargs):
        logger.debug('Creating new permission transaction')
        super(PermissionTransaction, self).__init__(
                requested_permission=requested_permission, sender_pubkey=sender_pubkey,  signature=signature, **kwargs
        )

        if type(sender_pubkey).__name__ == 'RsaKey':
            sender_pubkey = sender_pubkey.exportKey("DER")

        self.requested_permission = requested_permission
        self.sender_pubkey = sender_pubkey
        self.signature = signature

    def _get_informations_for_hashing(self):
        tuples = []
        for tuple in vars(self).items():
            if tuple[0] != 'signature':
                tuples.append(tuple)
        return '{!s}({!s})'.format(
            type(self).__name__,
            ', '.join(['{!s}={!r}'.format(*item) for item in tuples])
        )

    def validate(self):
        """
        checks if the transaction fulfills the requirements
        e.g. if enough positive votes were cast for an admission,
        signature matches, etc.
        """
        return self._verify_signature() # TODO check other requirements

    def _verify_signature(self):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.verify(message, self.signature, RSA.import_key(self.sender_pubkey))

    def _create_signature(self, private_key):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.sign(message, private_key)

    def sign(self, private_key):
        """creates a signature and adds it to the transaction"""
        if self.signature:
            logger.debug('Signature exists. Quit signing process.')
            return
        self.signature = self._create_signature(private_key)


if __name__ == "__main__":
    import os
    PUBLIC_KEY = RSA.import_key(open(".." + os.sep + ".." + os.sep + "tests" + os.sep + "testkey_pub.bin", "rb").read())
    PRIVATE_KEY = RSA.import_key(open(".." + os.sep + ".." + os.sep + "tests" + os.sep + "testkey_priv.bin", "rb").read())
    trans = PermissionTransaction(requested_permission=Permission.doctor, sender_pubkey=PUBLIC_KEY, timestamp=1234, version='1')
    print("REPRESENTATION:")
    print(repr(trans))
    # print(trans)
    trans.sign(PRIVATE_KEY)
    print("REPRESENTATION AFTER SIGNING:")
    print(repr(trans))
    # print(trans)
    print("TRANSACTION VALIDATION:")
    print(trans.validate())
    print("EVALUATED REPRESENTATION:")
    print(eval(repr(trans)))
