import hashlib

def hash_sha256(input: str) -> str:
    
    # NOTE: Hashing is a one way operation

    # String key needs to be encoded to bytes-like data
    enc = input.encode(encoding="utf-8")

    # Create the hashing object
    hash = hashlib.sha256()

    # Update the hash object with the byte-like encoded key
    hash.update(enc)

    # Transform the hashed key to a hexadecimal value
    hex_object = hash.hexdigest()
    return hex_object