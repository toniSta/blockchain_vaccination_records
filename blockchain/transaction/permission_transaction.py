import logging
import math
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
    def __init__(self, requested_permission, sender_pubkey, approvals=[], **kwargs):
        logger.debug("Creating new permission transaction")
        super(PermissionTransaction, self).__init__(
                requested_permission=requested_permission, sender_pubkey=sender_pubkey,
                approvals=approvals, **kwargs
        )

        if type(sender_pubkey).__name__ == "RsaKey":
            sender_pubkey = sender_pubkey.exportKey("DER")

        self.requested_permission = requested_permission
        self.sender_pubkey = sender_pubkey
        self.approvals = approvals

    def _get_informations_for_hashing(self):
        """Return a string representation of the contained data for hashing"""
        return str({
            "requested_permission": self.requested_permission,
            "sender_pubkey": self.sender_pubkey,
            "approvals": self.approvals,
            "timestamp": self.timestamp,
            "version": self.version
        })

    def validate(self, current_admissions):
        """Check if the transaction fulfills the requirements.

        Check if signarure matches,
        if enough positive votes were cast for an admission,
        etc.
        """
        if self.requested_permission is Permission.patient:
            return self._verify_signature()
        else:
            return self._verify_signature() and self._validate_approvals(current_admissions)

    def _validate_approvals(self, current_admissions):
        """Validate the includeded approvals of the transaction.

        Checks if there are duplicate approvals,
        if a sufficient number of approvals is present if the chain has at least 1 block,
        if the approval signatures are valid,
        if the approval was sent by a real admission nodes
        """
        if len(self.approvals) != len(set(self.approvals)):
            logger.debug("Transaction contains duplicate approvals.")
            return False
        if len(self.approvals) < math.ceil(len(current_admissions) / 2):
            logger.debug("Transaction does not contain the required number of approvals.")
            return False
        if len(self.approvals) != len([a for a in self.approvals if self._verify_approval_signature(a)]):
            logger.debug("Transaction contains approvals with invalid signature.")
            return False
        if len(self.approvals) != len([a for a in self.approvals if a[0] in current_admissions]):
            logger.debug("Transaction contains approvals from non-admission nodes.")
            return False
        return True

    def _verify_approval_signature(self, approval):
        approving_pubkey, signature = approval  # WONTFIX: susceptible to replay attacks
        return crypto.verify(approving_pubkey, signature, RSA.import_key(approving_pubkey))

