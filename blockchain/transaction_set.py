from orderedset import OrderedSet


class TransactionSet(object):
    """This class stores the clients transactions."""

    __instance = None

    def __new__(cls):
        """Create TransactionSet singleton instance"""
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        """Initialize transaction store."""
        self.store = OrderedSet()

    def add(self, transaction):
        self.store.add(transaction)

    def pop(self):
        """Remove and return a transaction from the set."""
        return self.store.pop(0)

    def clear(self):
        """Remove all transactions from the set."""
        self.store.clear()

    def discard(self, transaction):
        """Removes the transaction if it was present in the set."""
        self.store.discard(transaction)

    def contains(self, transaction):
        return self.store.__contains__(transaction)

    def __len__(self):
        return len(self.store)

    def __iter__(self):
        yield from self.store

    def __repr__(self):
        return self.store.__repr__()
