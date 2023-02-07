from argparse import ArgumentParser
from decouple import config
import uvicorn

from api.db.access import init_dbms_access

DBMS_DEFAULT_PORT = 3306
SERVER_DEFAULT_PORT = 8000

parser = ArgumentParser(description='Runs the Courter API server.')

parser.add_argument(
    '--setup',
    action='store_true',
    help='Run the servers setup script'
)

dbms_args = parser.add_argument_group('DBMS configuration')
dbms_args.add_argument('username', help='DBMS username')
dbms_args.add_argument('--pw', metavar='', help='DBMS password')
dbms_args.add_argument(
    '--dbms-port',
    type=int,
    metavar='',
    default=DBMS_DEFAULT_PORT,
    help=f'Port number of the DBMS server (default: {DBMS_DEFAULT_PORT})'
)
dbms_args.add_argument(
    '--echo',
    action='store_true',
    help='Enable the echoing of the communication sent to the DBMS'
)

server_args = parser.add_argument_group('Server configuration')
server_args.add_argument(
    '--api-port',
    type=int,
    metavar='',
    default=SERVER_DEFAULT_PORT,
    help=f'Port number the Courter API Server should run on (default: {SERVER_DEFAULT_PORT})'
)
server_args.add_argument(
    '--reload',
    action='store_true',
    help='Enable uvicorn\'s auto reload'
)

args = parser.parse_args()


def init_dbms():
    init_dbms_access(
        dbms=config('DBMS'),
        db_name=config('DB'),
        username=args.username,
        port=args.dbms_port,
        password=args.pw,
        use_async=not args.setup,
        echo=args.echo
    )


if args.setup:
    from setup import create_config, initial_db_setup, SetupAbortedException
    try:
        create_config()
        init_dbms()
        initial_db_setup()
        print('The setup has been completed successfully.')
    except SetupAbortedException:
        print('The setup has been aborted.')
else:
    init_dbms()


if __name__ == '__main__':
    uvicorn.run('api.main:app', port=args.api_port, reload=args.reload)
