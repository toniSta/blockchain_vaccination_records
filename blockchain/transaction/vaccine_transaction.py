import logging
from blockchain.transaction.transaction import TransactionBase
import blockchain.helper.cryptography as crypto
from Crypto.PublicKey import RSA

# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format="[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("blockchain")


class VaccineTransaction(TransactionBase):
    """This class depicts a registration of a vaccine."""

    def __init__(self, vaccine, sender_pub_key, signature=None, **kwargs):
        super(VaccineTransaction, self).__init__(
            vaccine=vaccine, signature=signature, sender_pub_key=sender_pub_key, **kwargs
        )

        if type(sender_pub_key).__name__ == "RsaKey":
            sender_pub_key = sender_pub_key.exportKey("DER")

        self.vaccine = vaccine
        self.sender_pub_key = sender_pub_key
        self.signature = signature

    def validate(self): # TODO Where does the key come from in the future?
        """
        checks if the transaction fulfills the requirements
        """
        #TODO Does the sender have permission to add vaccines?
        in_sender_key = RSA.import_key(self.sender_pub_key)
        return self._verify_signature(in_sender_key) # TODO check other requirements

    def sign(self, private_key):
        """creates a signature and adds it to the transaction"""
        if self.signature:
            logger.debug("Signature exists. Quit signing process.")
            return
        self.signature = self._create_signature(private_key)
        return self

    def _verify_signature(self, pupKey):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.verify(message, self.signature, pupKey)

    def _create_signature(self, private_key):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.sign(message, private_key)

    def _get_informations_for_hashing(self):
        string = "{}(version={}, timestamp={}, vaccine={}, sender_pub_key={})".format(
            type(self).__name__,
            self.version,
            self.timestamp,
            self.vaccine,
            self.sender_pub_key
        )
        return string


if __name__ == "__main__":
    import os
    PUBLIC_KEY = RSA.import_key(open(".." + os.sep + ".." + os.sep + "tests" + os.sep + "testkey_pub.bin", "rb").read())
    PRIVATE_KEY = RSA.import_key(open(".." + os.sep + ".." + os.sep + "tests" + os.sep + "testkey_priv.bin", "rb").read())
    trans = VaccineTransaction(vaccine="a vaccine", sender_pub_key=PUBLIC_KEY, timestamp=1234, version="1")
    print(repr(trans))
    trans.sign(PRIVATE_KEY)
    print(repr(trans))
    print(trans.validate())
    print(eval(repr(trans)))