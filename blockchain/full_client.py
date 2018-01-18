import logging

import random
import requests
from transaction_set import TransactionSet
import os
from .block import Block
from .chain import Chain
from .config import CONFIG
from .transaction import *


class FullClient(object):
    """docstring for FullClient"""
    def __init__(self):
        # Mock nodes by hard coding
        if os.getenv('NEIGHBORS_HOST_PORT'):
            neighbors_list = os.getenv('NEIGHBORS_HOST_PORT')
            neighbors_list = map(str.strip, neighbors_list.split(","))
            self.nodes = ["http://" + neighbor for neighbor in neighbors_list]
        else:
            self.nodes = ["http://127.0.0.1:9000"]
        self.chain = Chain()
        self.transaction_set = TransactionSet()
        self.invalid_transactions = set()

        self.recover_after_shutdown()

    def synchronize_blockchain(self):
        random_node = random.choice(self.nodes)
        last_block_remote = self._get_status_from_different_node(random_node)
        if last_block_remote.index == self.chain.last_block().index and \
           last_block_remote.hash == self.chain.last_block().hash:
            # blockchain is up-to-date
            return
        # TODO: implement synchronization
        if last_block_remote.index == self.chain.last_block().index and \
           last_block_remote.hash != self.chain.last_block().hash:
            # TODO: at least last block is wrong
            pass

        if last_block_remote.index != self.chain.last_block().index:
            # TODO: chain is outdated
            pass

    def create_next_block(self):
        new_block = Block(self.chain.last_block().get_block_information())

        for _ in range(CONFIG["block_size"]):
            # TODO: transaction validation
            # or do we want it before we add it to the transaction set
            if len(self.transaction_set):
                transaction = self.transaction_set.pop()
                if transaction:
                    new_block.add_transaction(transaction)
                else:
                    self.invalid_transactions.add(transaction)
            else:
                # Break if transaction set is empty
                break
        new_block.update_hash()
        return new_block

    def submit_block(self, block):
        # TODO: block validation
        if block:
            self.chain.add_block(block)
            self._broadcast_new_block(block)
            block.persist()

    def _broadcast_new_block(self, block):
        for node in self.nodes:
            route = node + "/new_block"
            requests.post(route, data=repr(block))

    def _get_status_from_different_node(self, node):
        random_node = random.choice(self.nodes)
        route = random_node + "/latest_block"
        block = requests.get(route)
        return Block(block.text)

    def recover_after_shutdown(self):
        # Steps:
        #   1. read in files from disk -> maybe in __init__ of chain
        #   2. sync with other node(s)
        pass

    def handle_new_transaction(self, transaction):
        transaction_object = eval(transaction)
        if self.transaction_set.contains(transaction_object):
            return  # Transaction was already received
        else:
            # TODO: check if it is in the chain already
            self.transaction_set.add(transaction_object)
            self._broadcast_new_transaction(transaction)

    def _broadcast_new_transaction(self, transaction):
        for node in self.nodes:
            route = node + "/new_transaction"
            requests.post(route, data=repr(transaction))

    def create_transaction(self):
        transaction_type = input("What kind of transaction should be created? (Vaccination/Vaccine/Permission)").lower()
        if transaction_type == "vaccination":
            vaccine = input("Which vaccine was given?").lower()
            doctor_pubkey = input("Enter doctors public key")
            patient_pubkey = input("Enter patients public key")
            transaction = VaccinationTransaction(doctor_pubkey, patient_pubkey, vaccine)
            print(transaction)
            sign_now = input("Sign transaction now? (Y/N)").lower()
            if sign_now == "y":
                doctor_privkey = input("Enter doctors private key")
                patient_privkey = input("Enter patients private key")
                transaction.sign(doctor_privkey, patient_privkey)
                print(transaction)
                return transaction
            elif sign_now == "n":
                return transaction
            else:
                print("Invalid option {}, aborting.".format(sign_now))
        elif transaction_type == "vaccine":
            vaccine = input("Which vaccine should be registered?").lower()
            admission_pubkey = input("Enter admissions public key")
            transaction = VaccineTransaction(vaccine, admission_pubkey)
            print(transaction)
            sign_now = input("Sign transaction now? (Y/N)").lower()
            if sign_now == "y":
                admission_privkey = input("Enter admission private key")
                transaction.sign(admission_privkey)
                print(transaction)
                return transaction
            elif sign_now == "n":
                return transaction
            else:
                print("Invalid option {}, aborting.".format(sign_now))
        elif transaction_type == "permission":
            permission_name = input("Which permission should be granted? (Patient/Doctor/Admission)").lower()
            permission = Permission[permission_name]
            sender_pubkey = input("Enter sender public key")
            transaction = PermissionTransaction(permission, sender_pubkey)
            print(transaction)
            if sign_now == "y":
                sender_privkey = input("Enter sender private key")
                transaction.sign(sender_privkey)
                print(transaction)
                return transaction
            elif sign_now == "n":
                return transaction
            else:
                print("Invalid option {}, aborting.".format(sign_now))
        else:
            print("Invalid option {}, aborting.".format(transaction_type))

