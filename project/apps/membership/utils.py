import os
import hashlib

from django.conf import settings

from .models import User


def generate_pin(length=9):
    hash_algorithm = 'sha512'
    m = getattr(hashlib, hash_algorithm)()
    m.update('secret-key'.encode('utf-8'))
    m.update(os.urandom(16))
    pin = str(int(m.hexdigest(), 16))[-length:]
    return pin


def sign_uid(uid):
    return User.signer.sign(uid)


def decode_uid_signature(signature, max_age=120):
    return User.signer.unsign(signature, max_age=max_age)

