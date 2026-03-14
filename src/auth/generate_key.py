import secrets

from auth.hashing import hash_sha256

def generate_keys() -> tuple[str, str]:

    """
    Returns a tuple, where [0] is the key, and [1] the hashed key
    """

    key = secrets.token_urlsafe(nbytes=32)
    hashed_key = hash_sha256(input=key)
    return (key, hashed_key)