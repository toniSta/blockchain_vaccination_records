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

    def __init__(self, vaccine, signature=None, **kwargs):
        super(VaccineTransaction, self).__init__(vaccine=vaccine, signature=signature, **kwargs)
        self.vaccine = vaccine
        self.signature = signature

    def validate(self, pubKey): # TODO Where does the key come from in the future?
        """
        checks if the transaction fulfills the requirements
        """
        return self._verify_signature(pubKey) # TODO check other requirements

    def _verify_signature(self, pupKey):
        message = crypto.get_bytes(repr(self.get_informations_for_hashing()))
        return crypto.verify(message, self.signature, pupKey)

    def _create_signature(self, private_key):
        message = crypto.get_bytes(repr(self.get_informations_for_hashing()))
        return crypto.sign(message, private_key)

    def sign(self, private_key):
        """creates a signature and adds it to the transaction"""
        if self.signature:
            logger.debug('Signature exists. Quit signing process.')
            return
        self.signature = self._create_signature(private_key)

    def get_informations_for_hashing(self):
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
    trans = VaccineTransaction(vaccine='a')
    print(repr(trans))
    print(trans.get_informations_for_hashing())
    trans.sign(PRIVATE_KEY)
    print(repr(trans))
    print(trans.get_informations_for_hashing())
    print(trans.validate(PUBLIC_KEY))