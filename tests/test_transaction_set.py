from blockchain.transaction_set import TransactionSet

import pytest


def test_transaction_set_is_singleton():
    set_1 = TransactionSet()
    set_2 = TransactionSet()
    set_2.add("tx1")
    assert id(set_1) == id(set_2)
    assert len(set_1) == 1


def test_adding_values():
    transaction_set = TransactionSet()
    assert len(transaction_set) == 0
    transaction_set.add("tx1")
    transaction_set.add("tx2")
    transaction_set.add("tx3")
    transaction_set.add("tx2")
    assert len(transaction_set) == 3


@pytest.fixture()
def transaction_set():
    tx_set = TransactionSet()
    tx_set.add("tx1")
    tx_set.add("tx2")
    yield tx_set


def test_contains(transaction_set):
    assert transaction_set.contains("tx1")
    assert not transaction_set.contains("tx3")


def test_clear(transaction_set):
    transaction_set.clear()
    assert len(transaction_set) == 0


def test_pop(transaction_set):
    transaction_set.pop()
    assert len(transaction_set) == 1
    tx2 = transaction_set.pop()
    assert tx2 is "tx2"
    assert len(transaction_set) == 0
    with pytest.raises(Exception) as excinfo:
        transaction_set.pop()
    assert excinfo.type == KeyError


def test_discard(transaction_set):
    transaction_set.discard("tx1")
    assert len(transaction_set) == 1
    transaction_set.discard("some random string")
    assert len(transaction_set) == 1


def test_iterator(transaction_set):
    for tx in transaction_set:
        assert tx is not None


def test_repr(transaction_set):
    assert repr(transaction_set) == "OrderedSet(['tx1', 'tx2'])"
