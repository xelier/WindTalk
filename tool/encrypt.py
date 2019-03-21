import os
from hashlib import sha256
from hmac import HMAC
import random


def encrypt_password(password, salt=None):
    if salt is None:
        #salt = os.urandom(8)
        salt = generate_random_str(random_length=8)

    assert 8 == len(salt)
    assert isinstance(salt, str)

    assert isinstance(password, str)

    result = password

    for i in range(10):
        result = HMAC(bytes(salt.encode('utf-8')), bytes(result.encode('utf-8')), sha256).digest()
        result = str(result)

    return salt + result


def validate_password(encrypted_password, input_password):
    return encrypted_password == encrypt_password(input_password, salt=encrypted_password[:8])


def generate_random_str(random_length=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str


if __name__ == '__main__':
    hashed = encrypt_password('hahahha')
    print(validate_password(hashed, 'hhh'))
    print(validate_password(hashed, 'hahahha'))
