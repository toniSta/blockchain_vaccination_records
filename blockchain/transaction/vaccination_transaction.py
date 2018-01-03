import logging
from blockchain.transaction.transaction import TransactionBase
import blockchain.helper.cryptography as crypto
from Crypto.PublicKey import RSA
import sys

# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format='[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger('blockchain')


class VaccinationTransaction(TransactionBase):
    """This class depicts a vaccination of a patient."""

    def __init__(self, doctorPubKey, patientPubKey, vaccine, doctorSignature=None, patientSignature=None, **kwargs):
        super(VaccinationTransaction, self).__init__(
            vaccine=vaccine, doctorSignature=doctorSignature, patientSignature=patientSignature, **kwargs
        )
        if type(doctorPubKey).__name__ == 'RsaKey':
            doctorPubKey = doctorPubKey.exportKey("DER")
        if type(patientPubKey).__name__ == 'RsaKey':
            patientPubKey = patientPubKey.exportKey("DER")

        self.vaccine = vaccine
        self.doctorSignature = doctorSignature
        self.patientSignature = patientSignature
        self.doctorPubKey = doctorPubKey
        self.patientPubKey = patientPubKey

    def validate(self): # TODO Where does the key come from in the future?
        """
        checks if the transaction fulfills the requirements
        """
        # TODO doctor key has doctor permission?
        # TODO vaccine is registered?
        # TODO patient key is registered -> won't implement
        bin_doctor_key = RSA.import_key(self.doctorPubKey)
        doctor_signature = self._verify_doctor_signature(bin_doctor_key)

        bin_patient_key = RSA.import_key(self.patientPubKey)
        patient_signature = self._verify_patient_signature(bin_patient_key)

        return doctor_signature and patient_signature

    def _verify_doctor_signature(self, pup_key):
        message = crypto.get_bytes(self._get_informations_for_hashing(True))
        return crypto.verify(message, self.doctorSignature, pup_key)

    def _verify_patient_signature(self, pup_key):
        message = crypto.get_bytes(self._get_informations_for_hashing(False))
        return crypto.verify(message, self.patientSignature, pup_key)

    def _create_doctor_signature(self, private_key):
        if self.doctorSignature:
            logger.debug('Doctor signature exists. Quit signing process.')
            return
        message = crypto.get_bytes(self._get_informations_for_hashing(True))
        return crypto.sign(message, private_key)

    def _create_patient_signature(self, private_key):
        if self.patientSignature:
            logger.debug('Patient signature exists. Quit signing process.')
            return

        print(str(self))
        print("Patient, do you want to sign the vaccination? (Y/N): ")
        reply = sys.stdin.read(1)
        reply = str(reply).lower()

        if reply == 'n':
            print("Aborting...")
            return None
        elif reply == 'y':
            message = crypto.get_bytes(self._get_informations_for_hashing(False))
            return crypto.sign(message, private_key)
        else:
            print("No valid input. Abort...")
            return None

    def sign(self, doctor_private_key, patient_private_key):
        """creates a signature and adds it to the transaction"""
        # TODO Finally the patient privatekey should be given by the patient
        self.doctorSignature = self._create_doctor_signature(doctor_private_key)
        self.patientSignature = self._create_patient_signature(patient_private_key)

    def _get_informations_for_hashing(self, as_doctor):
        tuples = []
        for tuple in vars(self).items():
            if tuple[0] != 'patientSignature':
                if not as_doctor:
                    tuples.append(tuple)
                if as_doctor and tuple[0] != 'doctorSignature':
                    tuples.append(tuple)

        return '{!s}({!s})'.format(
            type(self).__name__,
            ', '.join(['{!s}={!r}'.format(*item) for item in tuples])
        )


if __name__ == "__main__":
    import os
    PUBLIC_KEY = RSA.import_key(open(".." + os.sep + ".." + os.sep + "tests" + os.sep + "testkey_pub.bin", "rb").read())
    PRIVATE_KEY = RSA.import_key(open(".." + os.sep + ".." + os.sep + "tests" + os.sep + "testkey_priv.bin", "rb").read())
    trans = VaccinationTransaction(PUBLIC_KEY, PUBLIC_KEY, 'polio', timestamp=1234, version='1')
    print(repr(trans))
    trans.sign(PRIVATE_KEY, PRIVATE_KEY)
    print(repr(trans))
    print(trans.validate())
    print(eval(repr(trans)))