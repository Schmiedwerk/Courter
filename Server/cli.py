from argparse import ArgumentParser
import uvicorn

from api.db.login import set_login_data

DBMS_DEFAULT_PORT = 3306
SERVER_DEFAULT_PORT = 8000

parser = ArgumentParser(description='Runs the Courter API server.')

mysql_args = parser.add_argument_group('DBMS configuration')
mysql_args.add_argument('username', help='DBMS username')
mysql_args.add_argument('--pw',
                        metavar='',
                        help='DBMS password')
mysql_args.add_argument('--dbms-port',
                        type=int,
                        metavar='',
                        default=DBMS_DEFAULT_PORT,
                        help='Port number of the DBMS server '
                             f'(default: {DBMS_DEFAULT_PORT})')

server_args = parser.add_argument_group('Server configuration')
server_args.add_argument('--api-port',
                         type=int,
                         metavar='',
                         default=8000,
                         help='Port number the Courter API Server should run on '
                              f'(default: {SERVER_DEFAULT_PORT})')
server_args.add_argument('--reload',
                         action='store_true',
                         help='Enable uvicorn\'s auto reload')

args = parser.parse_args()

# login details for access to DBMS server on localhost
set_login_data(username=args.username, password=args.pw, port=args.dbms_port)

if __name__ == '__main__':
    uvicorn.run('api.main:app', port=args.api_port, reload=args.reload)
