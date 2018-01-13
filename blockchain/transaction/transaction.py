from abc import ABCMeta, abstractmethod
from blockchain.config import CONFIG
from blockchain.helper.cryptography import hexify
from time import time
from Crypto.PublicKey import RSA
import blockchain.helper.cryptography as crypto

class TransactionBase(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        self.version = kwargs.get("version") or CONFIG["version"]
        self.timestamp = kwargs.get("timestamp") or int(time())
        self.signature = None

    @abstractmethod
    def validate(self):
        raise NotImplementedError("Transaction must offer a validity check")

    @abstractmethod
    def _get_informations_for_hashing(self):
        raise NotImplementedError("Transaction must offer informations to be hashable")

    def _create_signature(self, private_key):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.sign(message, private_key)

    def _verify_signature(self):
        message = crypto.get_bytes(self._get_informations_for_hashing())
        return crypto.verify(message, self.signature, RSA.import_key(self.sender_pubkey))

    def sign(self, private_key):
        """Create cryptographic signature and add it to the transaction."""
        if self.signature:
            #logger.debug("Signature exists. Aborting signing process.")
            return
        self.signature = self._create_signature(private_key)
        return self

    def __str__(self):
        """
        This method returns a string representation of the object such that it is readable by human.
        The Class attributes will be ordered
        e.g. -----------------------
              Transaction: VaccineTransaction
              Signature: sfefsdf
              Timestamp: 1514903576
              Vaccine: 61
              Version: 0.0.1
            -----------------------
        """
        instance_member_list = []
        for item in vars(self).items():
            if type(item[1]).__name__ == "bytes":
                instance_member_list.append((item[0].title(), hexify(item[1])))
                continue

            if type(item[1]).__name__ == "list":
                modified_list = []
                for list_elem in item[1]:
                    if type(list_elem).__name__ == "tuple":
                        modified_tuple = []
                        for tuple_elem in list_elem:
                            if type(tuple_elem).__name__ == "bytes":
                                bytes_tuple_elem = hexify(tuple_elem)
                                modified_tuple.append(bytes_tuple_elem)
                            else:
                                modified_tuple.append(tuple_elem)
                        new_tuple = tuple(modified_tuple)
                        modified_list.append(new_tuple)
                    else:
                        modified_list.append(list_elem)
                instance_member_list.append((item[0].title(), modified_list))
                continue

            instance_member_list.append((item[0].title(), item[1]))
        instance_member_list.sort(key=lambda tup: tup[0])

        string = "-----------------------\n"
        string = string + "  Transaction: {}\n".format(type(self).__name__)
        for tuple_member in instance_member_list:
            string = string + "  {}: {}\n".format(*tuple_member)
        string = string + "-----------------------"
        return string


    def __repr__(self):
        """
        This method returns a string representation of the object such that eval() can recreate the object.
        The Class attributes will be ordered
        e.g. Class(attribute1="String", attribute2=3)
        """
        instance_member_list =[]
        for item in vars(self).items():
            instance_member_list.append(item)
        instance_member_list.sort(key=lambda tup: tup[0])

        return "{!s}({!s})".format(
            type(self).__name__,
            ", ".join(["{!s}={!r}".format(*item) for item in instance_member_list])
        )
