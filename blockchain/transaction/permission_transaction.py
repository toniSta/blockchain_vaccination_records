import logging
import blockchain.helper.cryptography as crypto
from Crypto.PublicKey import RSA
from enum import Enum
from blockchain.transaction.transaction import TransactionBase


# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format="[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("blockchain")


class Permission(Enum):
    """This class represents the available permissions"""

    patient = "patient"
    doctor = "doctor"
    admission = "admission"

    def __repr__(self):  # overriding to allow recreation with eval()
        return self.__str__()


class PermissionTransaction(TransactionBase):
    """This class represents the transaction of wallet permissions"""

    def __init__(self, requested_permission, sender_pubkey, approvals=[], signature=None, **kwargs):
        logger.debug("Creating new permission transaction")
        super(PermissionTransaction, self).__init__(
                requested_permission=requested_permission, sender_pubkey=sender_pubkey,
                approvals=approvals, signature=signature, **kwargs
        )

        if type(sender_pubkey).__name__ == "RsaKey":
            sender_pubkey = sender_pubkey.exportKey("DER")

        self.requested_permission = requested_permission
        self.sender_pubkey = sender_pubkey
        self.approvals = approvals
        self.signature = signature

    def _get_informations_for_hashing(self):
        """Return a string representation of the contained data for hashing"""
        return str({
            "requested_permission": self.requested_permission,
            "sender_pubkey": self.sender_pubkey,
            "approvals": self.approvals,
            "timestamp": self.timestamp,
            "version": self.version
        })

    def validate(self):
        """Check if the transaction fulfills the requirements.

        Check if signarure matches,
        if enough positive votes were cast for an admission,
        etc.
        """
        if self.requested_permission == Permission.patient:
            return self._verify_signature()
        else:
            return self._verify_signature() and self._validate_approvals()

    def _validate_approvals(self):
        """Validate the includeded approvals of the transaction.

        Checks if a sufficient number of approvals is present,
        if the approval signatures are valid and
        if the approval was sent by a real admission nodes.
        """
        if len(self.approvals) != len(set(self.approvals)):
            logger.debug("Transaction contains duplicate approvals.")
            return False
        if len(self.approvals) < 3:
            logger.debug("Transaction does not have enough approvals.")
            return False
        valid_sig_approvals = [a for a in self.approvals if self._verify_approval_signature(a)]
        if len(valid_sig_approvals) != len(self.approvals):
            logger.debug("Transaction contains invalid approvals.")
            return False
        return True

    def _verify_approval_signature(self, approval):
        approving_pubkey, signature = approval
        return crypto.verify(approving_pubkey, signature, RSA.import_key(approving_pubkey))

    def _verify_signature(self):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.verify(message, self.signature, RSA.import_key(self.sender_pubkey))

    def _create_signature(self, private_key):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.sign(message, private_key)

    def sign(self, private_key):
        """Create cryptographic signature and add it to the transaction."""
        if self.signature:
            logger.debug("Signature exists. Aborting signing process.")
            return
        self.signature = self._create_signature(private_key)
        return self
