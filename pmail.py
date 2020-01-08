import argparse
import pathlib
import os
import poplib
import sqlite3
import configparser
import inspect
import datetime

"""
    Necessary Variables, Constants, Class and others
"""

HOME_PATH = pathlib.Path.home()

FILE_PATH_CONFIGURATION = os.path.join(HOME_PATH, '.pmail')

CONFIGURATION_CHOICES = 'all backup server users'.split()

DEFAULT_CONFIGURATION_STRUCT = {
    'backup': {
        'path': HOME_PATH,
        'name': 'backup',
    },

    'server': {
        'host': 'localhost',
        'port': 110,
        'ssl': True
    },
    
    'users': {},
}

class TableDataBaseDict(dict):
    def __init__(self, path_db: str, name: str = None) -> None:
        self.name = name or self.__class__.__name__.lower()
        self.path_db = path_db

    def __get_connection(self):
        return sqlite3.connect(self.path_db)

    def create_table(self) -> None:
        connection = self.__get_connection()
        cursor = connection.cursor()

        fields = ','.join([
            f"{ field } TEXT" for field in self.keys()
        ])

        sql = f"CREATE TABLE IF NOT EXISTS { self.name } ( { fields } )"
        
        cursor.execute(sql)
        connection.commit()

        cursor.close()
        connection.close()
    
    def save(self) -> None:
        connection = self.__get_connection()
        cursor = connection.cursor()

        fields = ','.join(self.keys())

        values = ','.join([
            f"'{ value }'" for value in self.values()
        ])

        sql = f"INSERT INTO { self.name } ({ fields }) VALUES ({ values })"

        cursor.execute(sql)
        connection.commit()

        cursor.close()
        connection.close()

class EmailTable(TableDataBaseDict):
    def __init__(self, path_db: str) -> None:
        super().__init__(path_db, 'emails')

        # define the table fields
        self.setdefault('username', '')
        self.setdefault('sender', '')
        self.setdefault('date', '')
        self.setdefault('subject', '')
        self.setdefault('body_protocol', '')

class POPServer():
    def __init__(self, **kwargs) -> None:
        self.ssl = kwargs.get('ssl', False)
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', poplib.POP3_PORT)
        self.username = kwargs.get('username', '')
        self.password = kwargs.get('password', '')

        self.__server = None

    def connect(self):
        server_info = self.host, self.port

        self.__server = poplib.POP3(*server_info) if not self.ssl else poplib.POP3_SSL(*server_info)
        self.__server.user(self.username)
        self.__server.pass_(self.password)

    def get_emails(self):
        number_emails = len(self.__server.list()[1])

        return [self.__server.retr(i)[1] for i in range(1, number_emails + 1)]

    def get_sender(self, email):
        pass
"""
    Management Function

    This section is reserved to generic functions to manager configuration,
    database, backup and users
"""

def create_configuration_file(config: dict = {}) -> None:
    if os.path.exists(FILE_PATH_CONFIGURATION):
        print('Configuration already exists')
        return
    
    configuration = configparser.ConfigParser() 
    
    configuration.read_dict(
        config if config else DEFAULT_CONFIGURATION_STRUCT
    )

    with open(FILE_PATH_CONFIGURATION, 'w') as conf_file:
        configuration.write(conf_file)

    print('Configuration created with success')

def load_configuration() -> configparser.ConfigParser:
    if not os.path.exists(FILE_PATH_CONFIGURATION):
        print('File configuration not exists. You need run pmail.py config:create')
        return None

    configuration = configparser.ConfigParser()

    with open(FILE_PATH_CONFIGURATION, 'r') as conf_file:
        configuration.read_file(conf_file)
    
    return configuration

def create_name_to_database(configuration: configparser.ConfigParser) -> str:
    time_init = datetime.datetime.now().strftime(
        "%y-%m-%d %H-%M-%S"
    )

    backup_name = configuration.get('backup', 'name')

    return f"{ time_init }{ backup_name }.sqlite3"

"""
    Command Function

    This section is reserved to functions that process input arguments
"""
def command_create_configuration(**kwargs) -> None:
    new_configuration = configparser.ConfigParser()

    print("[BACKUP]")

    backup = 'path name'.split()
    new_configuration['backup'] = {
        option: input(f"Set { option }: ") for option in backup
    }

    print("\n[SERVER]")

    server = 'host port ssl'.split()
    new_configuration['server'] = {
        option: input(f"Set { option }: ") for option in server
    }

    print("\n[USERS]")

    new_configuration['users'] = {}

    new_configuration.write(
        open(FILE_PATH_CONFIGURATION, 'w')
    )

def command_get_configuration(**kwargs) -> None:
    opts = kwargs.get('opts')
    configuration = kwargs.get('configuration')

    # to list all options of a section
    if len(opts.input) == 1:
        section = opts.input[0]
        for option, value in configuration[section.lower()].items():
            print(f"{ option.lower() }: { value }")
    
    # to list option and value of a section
    if len(opts.input) > 1:
        section, option = opts.input
        print(configuration[section][option])
    
    # to list all sections
    if len(opts.input) == 0:
        for section, options in configuration.items():
            if section.lower() == 'default':
                continue
            
            output = f"[{ section.upper() }]\n" + "\n".join([
                f"{ option }: { value }" for option, value in options.items()
            ])

            print(output, "\n")

def command_set_configuration(**kwargs) -> None:
    section, option, value = kwargs.get('opts').input
    configuration = kwargs.get('configuration')

    configuration.set(section, option, value)

    configuration.write(
        open(FILE_PATH_CONFIGURATION, 'w')
    )

def command_adduser_configuration(**kwargs) -> None:
    opts = kwargs.get('opts')

    configuration = kwargs.get('configuration')
    configuration.set('users', opts.username, opts.password)

    configuration.write(
        open(FILE_PATH_CONFIGURATION, 'w')
    )

def command_run_backup(**kwargs):
    email_table = kwargs.get('email_table')
    email_table.create_table()

"""
    Define Input Arguments
"""
arguments = argparse.ArgumentParser('PMail', description='Mail Backupper')
sub_arguments = arguments.add_subparsers()

# config:create
arg_create_configuration = sub_arguments.add_parser(
    'config:create',
    help='create file configuration'
)
arg_create_configuration.set_defaults(
    command=command_create_configuration
)

# config:get
arg_get_configuration = sub_arguments.add_parser(
    'config:get',
    help='get configuration value'
)
arg_get_configuration.add_argument(
    'input',
    nargs='*',
    help='get the all, section or option',
)
arg_get_configuration.set_defaults(
    command=command_get_configuration
)

# config:set
arg_set_configuration = sub_arguments.add_parser(
    'config:set',
    help='set configuration value'
)
arg_set_configuration.add_argument(
    'input',
    nargs=3,
    help='set option value',
)
arg_set_configuration.set_defaults(
    command=command_set_configuration
)

# config:adduser
arg_adduser_configuration = sub_arguments.add_parser(
    'config:adduser',
    help='add user to backup'
)
arg_adduser_configuration.add_argument(
    'username',
    type=str,
    help='username@hostname.com',
)
arg_adduser_configuration.add_argument(
    'password',
    type=str,
    help='password for user',
)
arg_adduser_configuration.set_defaults(
    command=command_adduser_configuration
)

# backup:run
arg_run_backup = sub_arguments.add_parser(
    'backup:run',
    help='make backup'
)
arg_run_backup.set_defaults(
    command=command_run_backup
)

"""
    Main Function
"""
def main() -> None:
    global arguments

    configuration = load_configuration()

    path_db = create_name_to_database(configuration)
    email_table = EmailTable(path_db)

    opts = arguments.parse_args()

    if getattr(opts, 'command', None):
        opts.command(opts=opts, configuration=configuration, email_table=email_table)
    else:
        arguments.print_help()

if __name__ == '__main__':
    main()