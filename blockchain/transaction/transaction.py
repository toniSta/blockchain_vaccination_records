from abc import ABCMeta, abstractmethod
from blockchain.config import CONFIG
from blockchain.helper.cryptography import hexify

class TransactionBase(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        self.version = kwargs.get('version') or CONFIG['version']

    @abstractmethod
    def validate(self):
        raise NotImplementedError("Transaction must offer a validity check")

    def __str__(self):
        list = []
        for item in vars(self).items():
            if type(item[1]).__name__ == 'bytes':
                item[1] = hexify(item[1])
            list.append(item)
        list.sort(key=lambda tup: tup[0])

        string = '-----------------------\n'
        string = string + '  Transaction: {}\n'.format(type(self).__name__)
        for tuple in list:
            string = string + '  {}: {}\n'.format(*tuple)
        string = string + '-----------------------'
        return string


    def __repr__(self):
        """
        This method returns a string representation of the object such that eval() can recreate the object.
        The Class attributes will be ordered
        e.g. Class(attribute1='String', attribute2=3)
        """
        list =[]
        for item in vars(self).items():
            list.append(item)
        list.sort(key=lambda tup: tup[0])

        return '{!s}({!s})'.format(
            type(self).__name__,
            ', '.join(['{!s}={!r}'.format(*item) for item in list])
        )
