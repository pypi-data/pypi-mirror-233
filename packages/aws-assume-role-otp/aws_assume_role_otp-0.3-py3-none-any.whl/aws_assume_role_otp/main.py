import typer

from aws_assume_role_otp.config import initial_config, is_first_run
from aws_assume_role_otp.credentials import (
    configure_credentials,
    credentials_configured,
    get_credentials,
    get_roles,
    prompt_role,
    add_role as call_add_role,
    remove_role as call_remove_role,
)
from aws_assume_role_otp.sts import assume_selected_role

app = typer.Typer()


@app.command()
def assume_role(add_role: bool = False, remove_role: bool = False) -> None:
    if is_first_run():
        initial_config()
    if not credentials_configured():
        configure_credentials()
    credentials = get_credentials()
    roles = get_roles()
    
    if add_role:
        call_add_role(credentials, roles)
    elif remove_role:
        call_remove_role(credentials, roles)
    else:
        selected_role = prompt_role(roles)
        assume_selected_role(credentials, selected_role)


if __name__ == "__main__":
    app()
