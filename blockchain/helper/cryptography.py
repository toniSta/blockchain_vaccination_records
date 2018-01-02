from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

def get_bytes(message):
    return bytes(message, encoding="utf8")

def generate_keypair(keysize=2048):
    """
    generates a new keypair using a random seed and the RSA algorith
    """
    random = Random.new().read
    key = RSA.generate(keysize, random)
    public, private  = key.publickey(), key
    return public, private

def sign(message, private_key):
    """
    creates a signature for the message with the given private key,
    expects message as a byte string
    """
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.sign(digest)

def verify(message, signature, public_key):
    signer = PKCS1_v1_5.new(public_key)
    """
    verifies the message with the given signature and public key,
    expects message as a byte string
    """
    digest = SHA256.new()
    digest.update(message)
    return signer.verify(digest, signature)


def hexify(s):
    if s is None:
        return ""
    else:
        return s.hex()