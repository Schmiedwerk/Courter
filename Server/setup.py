from secrets import token_hex
import qprompt

from api.db.access import DB_DRIVERS, get_engine, get_session_cls
from api.db.models import Base, Admin
from api.auth import get_password_hash
from api.schemes.user import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH


class SetupAbortedException(Exception):
    pass


def create_config():
    print('\nWarnings:')
    print(' - You need an empty database for the Courter API server before running the setup.')
    print(' - Continuing will override any current configuration.\n')
    run_setup = qprompt.ask_yesno('Do you want to run the setup? ')
    if not run_setup:
        raise SetupAbortedException()

    config = dict()

    print('Please pick the DBMS you want to use.')
    menu = qprompt.Menu()
    for dbms in DB_DRIVERS.keys():
        menu.enum(dbms)
    config['DBMS'] = menu.show(header='Database Management Systems', returns='desc')

    config['DB'] = qprompt.ask_str('What is the name of your Courter API database? ')

    generate_key = qprompt.ask_yesno(
        'Would you like the setup to generate a key for signing JWTs (recommended)? '
    )
    if generate_key:
        key = token_hex(32)
    else:
        key = qprompt.ask_str('Please enter your key.')
    config['KEY'] = key

    with open('.env', 'w') as config_file:
        config_file.write(
            '\n'.join(f'{key}={value}' for key, value in config.items())
        )


def initial_db_setup():
    Base.metadata.create_all(get_engine())
    _create_admin()


def _create_admin():
    admin_name = qprompt.ask_str(
        f'Please enter a username for the first administrator account'
        f' ({USERNAME_MIN_LENGTH} - {USERNAME_MAX_LENGTH} characters) ',
        valid=lambda name: USERNAME_MIN_LENGTH <= len(name) <= USERNAME_MAX_LENGTH
    )
    while True:
        password = qprompt.ask_pass(
            msg=f"Enter the administrator's password ({PASSWORD_MIN_LENGTH} - {PASSWORD_MAX_LENGTH} characters) ",
            valid=lambda pw: PASSWORD_MIN_LENGTH <= len(pw) <= PASSWORD_MAX_LENGTH
        )

        password_reenter = qprompt.ask_pass(msg='Re-enter the password for confirmation ')

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
