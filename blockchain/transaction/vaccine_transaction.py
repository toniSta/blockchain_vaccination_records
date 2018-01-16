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

    def __init__(self, vaccine, sender_pubkey, signature=None, **kwargs):
        super(VaccineTransaction, self).__init__(
            vaccine=vaccine, signature=signature, sender_pubkey=sender_pubkey, **kwargs
        )

        if type(sender_pubkey).__name__ == "RsaKey":
            sender_pubkey = sender_pubkey.exportKey("DER")

        self.vaccine = vaccine
        self.sender_pubkey = sender_pubkey
        self.signature = signature

    def validate(self): # TODO Where does the key come from in the future?
        """
        checks if the transaction fulfills the requirements
        """
        #TODO Does the sender have permission to add vaccines?
        in_sender_key = RSA.import_key(self.sender_pubkey)
        return self._verify_signature() # TODO check other requirements

    def _create_signature(self, private_key):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.sign(message, private_key)

    def _get_informations_for_hashing(self):
        string = "{}(version={}, timestamp={}, vaccine={}, sender_pub_key={})".format(
            type(self).__name__,
            self.version,
            self.timestamp,
            self.vaccine,
            self.sender_pubkey
        )
        return string
