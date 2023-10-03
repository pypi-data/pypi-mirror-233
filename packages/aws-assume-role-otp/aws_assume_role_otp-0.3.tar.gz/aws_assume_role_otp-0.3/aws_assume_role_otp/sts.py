import configparser
import os

import boto3
import botocore
import pyotp
from InquirerPy.utils import color_print


def is_access_key_valid(access_key_id: str, secret_access_key: str) -> bool:
    client = boto3.client(
        "sts", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )
    try:
        response = client.get_caller_identity()
        return True
    except botocore.exceptions.ClientError as e:
        print(e)
        return False


def can_assume_role(
    access_key_id, secret_access_key, role_arn: str, serial: str, token: str
) -> bool:
    client = boto3.client(
        "sts", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )
    try:
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=f"{os.environ['USER']}-validate-assume-role",
            SerialNumber=serial,
            TokenCode=token,
        )
        return True
    except botocore.exceptions.ClientError as e:
        print(e)
        return False


def update_credentials_file(
    access_key_id: str, secret_access_key: str, session_token: str, profile_name: str
):
    credentials_path = os.path.expanduser("~/.aws/credentials")
    if not os.path.exists(credentials_path):
        with open(credentials_path, "w") as f:
            pass
    config = configparser.ConfigParser()
    config.read(credentials_path)
    if profile_name not in config.sections():
        config.add_section(profile_name)

    config[profile_name]["aws_access_key_id"] = access_key_id
    config[profile_name]["aws_secret_access_key"] = secret_access_key
    config[profile_name]["aws_session_token"] = session_token
    with open(credentials_path, "w") as f:
        config.write(f)


def assume_selected_role(credentials: "Credentials", role: "Role") -> None:
    color_print([("#ADFF2F", "Assuming role: "), ("#1E90FF", role.arn)])
    client = boto3.client(
        "sts",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
    )
    totp = pyotp.TOTP(credentials.otp)
    response = client.assume_role(
        RoleArn=role.arn,
        RoleSessionName=f"{os.environ['USER']}-session-{role.profile or ''}",
        SerialNumber=credentials.serial,
        TokenCode=totp.now(),
    )

    if role.profile != "":
        update_credentials_file(
            response["Credentials"]["AccessKeyId"],
            response["Credentials"]["SecretAccessKey"],
            response["Credentials"]["SessionToken"],
            role.profile,
        )
        color_print(
            [("#ADFF2F", "Profile updated. To activate the profile run the command")]
        )
        color_print([("#1E90FF", f"export AWS_PROFILE={role.profile}")])
    else:
        color_print(
            [
                (
                    "#1E90FF",
                    f"export AWS_ACCESS_KEY_ID={response['Credentials']['AccessKeyId']}",
                )
            ]
        )
        color_print(
            [
                (
                    "#1E90FF",
                    f"export AWS_SECRET_ACCESS_KEY={response['Credentials']['SecretAccessKey']}",
                )
            ]
        )
        color_print(
            [
                (
                    "#1E90FF",
                    f"export AWS_SESSION_TOKEN={response['Credentials']['SessionToken']}",
                )
            ]
        )
