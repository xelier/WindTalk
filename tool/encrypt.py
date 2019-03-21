import os
from hashlib import sha256
from hmac import HMAC


def encrypt_password(password, salt = None):
    if salt is None:
        salt = os.urandom(8)

    assert 8 == len(salt)
    assert isinstance(salt, str)

    assert isinstance(password, str)

    result = password

    for i in range(10):
        result = HMAC(result, salt, sha256).digest()

    return salt + result


def validate_password(encrypted_password, input_password):
    return encrypted_password == encrypt_password(input_password, salt=encrypted_password[:8])

