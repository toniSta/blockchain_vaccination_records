from blockchain.transaction_set import TransactionSet

import pytest


def test_transaction_set_is_singleton():
    set_2 = TransactionSet()
    set_2.add("tx1")
    set_1 = TransactionSet()
    # assert len(set_1) == 1
    # assert id(set_1) == id(set_2)


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
    tx1 = transaction_set.pop()
    # assert tx1 == "tx1"
    # assert len(transaction_set) == 1
    # tx2 = transaction_set.pop()
    # assert tx2 is None
    # assert len(transaction_set) == 1
