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

    def validate(self, admissions, doctors, vaccines):
        """Check if the transaction fulfills the requirements.

        Check if signature matches,
        if enough positive votes were cast for an admission,
        etc.
        """
        if self.requested_permission is Permission.patient:
            return self._verify_signature()
        else:
            return self._verify_signature() and self._validate_approvals(chain_size, admissions)

    def _validate_approvals(self, chain_size, current_admissions):
        """Validate the includeded approvals of the transaction.

        Checks if there are duplicate approvals,
        if a sufficient number of approvals is present if the chain has at least 1 block,
        if the approval signatures are valid,
        if the approval was sent by a real admission nodes
        """
        if len(self.approvals) != len(set(self.approvals)):
            logger.debug("Transaction contains duplicate approvals.")
            return False
        if chain_size > 0 and len(self.approvals) < 3: # TODO: dynamically set or have magic number?
            logger.debug("Transaction does not have enough approvals.")
            return False
        valid_approvals = [a for a in self.approvals if self._verify_approval_signature(a)]
        if chain_size > 0:
            valid_approvals = [a for a in valid_approvals if a[0] in current_admissions]
        if len(valid_approvals) != len(self.approvals):
            logger.debug("Transaction contains invalid approvals.")
            return False
        return True

    def _verify_approval_signature(self, approval):
        approving_pubkey, signature = approval
        return crypto.verify(approving_pubkey, signature, RSA.import_key(approving_pubkey))

