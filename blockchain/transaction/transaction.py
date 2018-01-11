from abc import ABCMeta, abstractmethod
from blockchain.config import CONFIG
from blockchain.helper.cryptography import hexify
from time import time

class TransactionBase(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        self.version = kwargs.get("version") or CONFIG["version"]
        self.timestamp = kwargs.get("timestamp") or int(time())

    @abstractmethod
    def validate(self):
        raise NotImplementedError("Transaction must offer a validity check")

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
