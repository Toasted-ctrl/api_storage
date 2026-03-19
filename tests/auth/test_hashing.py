from auth.hashing import hash_sha256

def test_hash_sha256():
    test_input = "TEST_INPUT"
    hash = hash_sha256(input=test_input)
    assert hash == "0778437d471096138db7221c2894daf76a58180b525f6b53f8853eb1ed51a09f"