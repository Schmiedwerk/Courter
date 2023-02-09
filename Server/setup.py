import pyinputplus as pyip
from secrets import token_hex
from getpass import getpass

from api.db.access import DB_APIS, get_engine, get_session_cls
from api.db.models import Base, Admin
from api.auth import get_password_hash


class SetupAbortedException(Exception):
    pass


def create_config():
    print('\nWarnings:')
    print(' - You need an empty database for the Courter API server before running the setup.')
    print(' - Continuing will override any current configuration.\n')
    aborted = pyip.inputYesNo(
        prompt='Do you want to run the setup? [yes / no]\n'
    ) == 'no'
    if aborted:
        raise SetupAbortedException()

    config = dict()

    config['DBMS'] = pyip.inputMenu(
        choices=tuple(DB_APIS.keys()),
        prompt='Please pick the DBMS you want to use.\n',
        lettered=True
    )

    config['DB'] = pyip.inputStr(
        prompt='What is the name of your Courter API database?\n'
    )

    generate_key = pyip.inputYesNo(
        prompt='Would you like the setup to generate a key for signing JWTs? '
               '[yes (recommended) / no]\n'
    ) == 'yes'

    if generate_key:
        key = token_hex(32)
    else:
        key = pyip.inputStr(prompt='Please enter your key.\n')

    config['KEY'] = key

    with open('.env', 'w') as config_file:
        config_file.write(
            '\n'.join(f'{key}={value}' for key, value in config.items())
        )


def initial_db_setup():
    Base.metadata.create_all(get_engine())
    _create_admin()


def _create_admin():
    admin_name = pyip.inputStr('Please enter a username for the first administrator account.\n')
    while True:
        password = getpass("Enter the administrator's password.\n")
        password_reenter = getpass('Re-enter the password for confirmation.\n')

        if password == password_reenter:
            break
        print("The passwords don't match. Please retry.")

    password_hash = get_password_hash(password)
    admin = Admin(admin_name, password_hash)

    with get_session_cls()() as session:
        session.add(admin)
        session.commit()


if __name__ == '__main__':
    print("Please use the command line interface with the '--setup' option to run the setup.")
