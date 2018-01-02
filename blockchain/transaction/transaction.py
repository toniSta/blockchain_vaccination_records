from abc import ABCMeta, abstractmethod

class TransactionBase(metaclass=ABCMeta):
    @abstractmethod
    def validate(self):
        raise NotImplementedError("Transaction must offer a validity check")

    @abstractmethod
    def __str__(self):
        raise NotImplementedError("Transaction must have a printable representation")
