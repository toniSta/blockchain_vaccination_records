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

    def validate(self, admissions, doctors, vaccines):
        if self.sender_pubkey not in admissions:
            logger.debug("admission is not registered.")
            self.validation_text = "admission is not registered."
            return False
        return self._verify_signature()

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
