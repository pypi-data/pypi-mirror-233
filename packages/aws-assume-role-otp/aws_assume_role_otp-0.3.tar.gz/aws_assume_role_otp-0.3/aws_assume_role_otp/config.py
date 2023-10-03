import json
import os
import random
import string
from enum import Enum

import appdirs
from InquirerPy import inquirer
from InquirerPy.utils import color_print

CONFIG_DIR = appdirs.user_data_dir("aws-assume-role-otp")
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, "config.json")


class Config:
    def __init__(self, key_path: str, salt: bytes):
        self.key_path = key_path
        self.salt = salt


def is_first_run() -> bool:
    return not os.path.exists(CONFIG_FILE_PATH)


def initial_config() -> None:
    color_print([("#1E90FF", "First time run configuration")])
    key_path = inquirer.text(
        message="Where do you want to store your encrypted key?",
        default=f"{os.path.expanduser( '~' )}/.aws-assume-role-otp.key",
        validate=lambda result: os.access(os.path.dirname(result), os.W_OK),
        invalid_message="The path is not writeable",
    ).execute()
    with open(CONFIG_FILE_PATH, "w") as f:
        salt = "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
        f.write(json.dumps({"key_path": key_path, "salt": salt}))


def get_config() -> Config:
    with open(CONFIG_FILE_PATH, "r") as f:
        config = json.loads(f.read())
        return Config(config["key_path"], config["salt"].encode())
