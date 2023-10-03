import base64
import hashlib
import os

from cryptography.fernet import Fernet

from aws_assume_role_otp.config import get_config

hash = ""


def get_hash() -> bytes:
    global hash
    if hash != "":
        return hash.encode()

    sha256_hash = hashlib.sha256()
    files = [
        f
        for f in os.listdir(os.path.dirname(__file__))
        if os.path.isfile(os.path.dirname(__file__) + "/" + f)
    ]
    for file in files:
        with open(os.path.dirname(__file__) + "/" + file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    hash = sha256_hash.hexdigest()[:16]
    return hash.encode()


def encrypt(plain: str) -> str:
    fernet = Fernet(base64.urlsafe_b64encode(get_hash() + get_config().salt))
    return fernet.encrypt(plain.encode()).decode()


def decrypt(encrypted: str) -> str:
    fernet = Fernet(base64.urlsafe_b64encode(get_hash() + get_config().salt))
    return fernet.decrypt(encrypted).decode()
