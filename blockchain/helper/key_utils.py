"""This module provides helper functions for handling private/public keys.
"""

from Crypto.PublicKey import RSA

def bytestring_to_rsa(key):
    return RSA.import_key(key)

def bytestring_to_hex(key):
    return key.hex()

def hex_to_bytestring(key):
    return bytes.fromhex(key)

def hex_to_rsa(key):
    return bytestring_to_rsa(hex_to_bytestring(key))

def rsa_to_bytestring(key):
    return key.exportKey("DER")

def rsa_to_hex(key):
    return bytestring_to_hex(rsa_to_bytestring(key))