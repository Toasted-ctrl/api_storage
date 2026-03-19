import hashlib

from auth.generate_key import generate_keys

def test_generate_key():
    keys = generate_keys()
    unhashed_key = keys[0]
    hashed_key = keys[1]
    expected_hash = hashlib.sha256(unhashed_key.encode()).hexdigest()
    assert isinstance(unhashed_key, str)
    assert unhashed_key != hashed_key
    assert hashed_key == expected_hash