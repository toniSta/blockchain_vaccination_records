import logging
from blockchain.transaction.transaction import TransactionBase
import blockchain.helper.cryptography as crypto
from Crypto.PublicKey import RSA

# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format='[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger('blockchain')


class VaccineTransaction(TransactionBase):
    """This class depicts a registration of a vaccine."""

    def __init__(self, vaccine, senderPubKey, signature=None, **kwargs):
        super(VaccineTransaction, self).__init__(
            vaccine=vaccine, signature=signature, senderPubKey=senderPubKey, **kwargs
        )

        if type(senderPubKey).__name__ == 'RsaKey':
            senderPubKey = senderPubKey.exportKey("DER")

        self.vaccine = vaccine
        self.senderPubKey = senderPubKey
        self.signature = signature

    def validate(self): # TODO Where does the key come from in the future?
        """
        checks if the transaction fulfills the requirements
        """
        #TODO Does the sender have permission to add vaccines?
        in_sender_key = RSA.import_key(self.senderPubKey)
        return self._verify_signature(in_sender_key) # TODO check other requirements

    def sign(self, private_key):
        """creates a signature and adds it to the transaction"""
        if self.signature:
            logger.debug('Signature exists. Quit signing process.')
            return
        self.signature = self._create_signature(private_key)

    def _verify_signature(self, pupKey):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.verify(message, self.signature, pupKey)

    def _create_signature(self, private_key):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.sign(message, private_key)

    def _get_informations_for_hashing(self):
        tuples = []
        for tuple in vars(self).items():
            if tuple[0] != 'signature':
                tuples.append(tuple)
        return '{!s}({!s})'.format(
            type(self).__name__,
            ', '.join(['{!s}={!r}'.format(*item) for item in tuples])
        )


if __name__ == "__main__":
    import os
    PUBLIC_KEY = RSA.import_key(open(".." + os.sep + ".." + os.sep + "tests" + os.sep + "testkey_pub.bin", "rb").read())
    PRIVATE_KEY = RSA.import_key(open(".." + os.sep + ".." + os.sep + "tests" + os.sep + "testkey_priv.bin", "rb").read())
    trans = VaccineTransaction(vaccine='a vaccine', senderPubKey=PUBLIC_KEY, timestamp=1234, version='1')
    print(repr(trans))
    trans.sign(PRIVATE_KEY)
    print(repr(trans))
    print(trans.validate())
    print(eval(repr(trans)))