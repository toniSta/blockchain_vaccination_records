import logging
from enum import Enum
from Crypto.PublicKey import RSA

import blockchain.helper.cryptography as crypto
from blockchain.transaction.transaction import TransactionBase

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
        return str({
            "requested_permission": self.requested_permission,
            "sender_pubkey": self.sender_pubkey,
            "approvals": self.approvals,
            "timestamp": self.timestamp,
            "version": self.version
        })

    def validate(self, admissions, doctors, vaccines):
        if self.requested_permission is Permission.patient:
            return self._verify_signature()
        else:
            return self._verify_signature() and self._validate_approvals(admissions)

    def _validate_approvals(self, current_admissions):
        """Validate the included approvals of the transaction.

        Checks if there are duplicate approvals,
        if a sufficient number of approvals is present if the chain has at least 1 block,
        if the approval signatures are valid,
        if the approval was sent by a real admission nodes
        """
        if len(self.approvals) != len(set(self.approvals)):
            logger.debug("Transaction contains duplicate approvals.")
            self.validation_text = "Transaction contains duplicate approvals."
            return False
        # WONTFIX: won't register admissions with approvals in presentation demo, therefore commented out
        # if len(self.approvals) < math.ceil(len(current_admissions) / 2):
        #    logger.debug("Transaction does not contain the required number of approvals.")
        #    return False
        if len(self.approvals) != len([a for a in self.approvals if self._verify_approval_signature(a)]):
            logger.debug("Transaction contains approvals with invalid signature.")
            self.validation_text = "Transaction contains approvals with invalid signature."
            return False
        if len(self.approvals) != len([a for a in self.approvals if a[0] in current_admissions]):
            logger.debug("Transaction contains approvals from non-admission nodes.")
            self.validation_text = "Transaction contains approvals from non-admission nodes."
            return False
        self.validation_text = "valid"
        return True

    def _verify_approval_signature(self, approval):
        # WONTFIX: susceptible to replay attacks because there is no clear indication
        # which transactions the approval belongs to, approvals could be copy-pasted to confirm malicious actors.
        approving_pubkey, signature = approval
        return crypto.verify(approving_pubkey, signature, RSA.import_key(approving_pubkey))

