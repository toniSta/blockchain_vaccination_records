"""This module provides helper functions for handling private/public keys.
"""

from Crypto.PublicKey import RSA


def bytes_to_rsa(key):
    return RSA.import_key(key)


def bytes_to_hex(key):
    return key.hex() if key else ""


def hex_to_bytes(key):
    return bytes.fromhex(key)


def hex_to_rsa(key):
    return bytes_to_rsa(hex_to_bytes(key))


def rsa_to_bytes(key):
    return key.exportKey("DER")


def rsa_to_hex(key):
    return bytes_to_hex(rsa_to_bytes(key))


def load_bytes_from_pem(key_path):
    return rsa_to_bytes(load_rsa_from_pem(key_path))


def load_hex_from_pem(key_path):
    return rsa_to_hex(load_rsa_from_pem(key_path))


def load_rsa_from_pem(key_path):
    with open(key_path, "rb") as key_file:
        return RSA.import_key(key_file.read())


def write_key_to_pem(key, key_path):
    with open(key_path, "wb") as key_file:
        if type(key).__name__ == "bytes":
            key = bytes_to_rsa(key)
        elif type(key).__name__ == "str":
            key = hex_to_rsa(key)
        key_file.write(key.exportKey())
