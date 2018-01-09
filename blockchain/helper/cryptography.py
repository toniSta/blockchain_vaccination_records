from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

def get_bytes(message):
    return bytes(message, encoding="utf8")

def generate_keypair(keysize=2048):
    """Generate a new keypair using a random seed and the RSA algorithm."""
    random = Random.new().read
    key = RSA.generate(keysize, random)
    public, private  = key.publickey(), key
    return public, private

def sign(message, private_key):
    """Create a cryptographic signature for the given message and private key.

    Expects message as a byte string, use get_bytes() to convert.
    """
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.sign(digest)

def verify(message, signature, public_key):
    """Verifies the message with the given signature and public key.

    Expects message as a byte string, use get_bytes() to convert.
    """
    signer = PKCS1_v1_5.new(public_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.verify(digest, signature)


def hexify(s):
    return s.hex() if s else ""
