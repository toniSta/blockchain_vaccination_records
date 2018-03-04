from orderedset import OrderedSet


class TransactionSet(object):
    """This class stores the clients transactions."""

    class __TransactionSet:
        def __init__(self):
            """Initialize transaction store."""
            self.store = OrderedSet()

        def add(self, transaction):
            self.store.add(transaction)

        def add_multiple(self, transaction_list):
            """Add multiple transactions to the set.

            Since the transactions are re-added to the set (they were in it once),
            we add them at the front of the existing set.
            """
            transaction_list = OrderedSet(transaction_list)
            self.store = transaction_list.union(self.store)

        def contains(self, transaction):
            return self.store.__contains__(transaction)

        def pop(self):
            """Remove and return a transaction from the set."""
            try:
                return self.store.pop(0)
            # Catch KeyError if set is empty
            except KeyError:
                return None

        def discard(self, transaction):
            """Remove the transaction if it was present in the set."""
            self.store.discard(transaction)

        def discard_multiple(self, transaction_list):
            """Remove multiple transactions from the set."""
            [self.discard(tx) for tx in transaction_list]

        def clear(self):
            """Remove all transactions from the set."""
            self.store.clear()

        def __len__(self):
            return len(self.store)

        def __iter__(self):
            yield from self.store

        def __repr__(self):
            return self.store.__repr__()

    __instance = None

    def __new__(cls, load_persisted=True):
        """Create a singleton instance of the chain."""
        if cls.__instance is None:
            cls.__instance = TransactionSet.__TransactionSet()
        return cls.__instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
