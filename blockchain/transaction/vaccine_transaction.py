import logging
from blockchain.transaction.transaction import TransactionBase

# Needs to be moved later
logging.basicConfig(level=logging.DEBUG,
                    format='[ %(asctime)s ] %(levelname)-7s %(name)-s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger('blockchain')


class VaccineTransaction(TransactionBase):

    def __init__(self, **kwargs):
        super(VaccineTransaction, self).__init__(**kwargs)
        self.vaccine = kwargs.get('vaccine')
        self.signature = kwargs.get('signature')

    def validate(self):  # TODO
        return True



if __name__ == "__main__":
    print(str(VaccineTransaction(vaccine='a', signature='sfefsdf')))
