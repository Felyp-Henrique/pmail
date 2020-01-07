import argparse
import pathlib
import os
import poplib
import sqlite3
import configparser

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

"""
    Management Function

    This section is reserved to generic functions to manager configuration,
    database, backup and users
"""

def create_configuration_file(config={}):
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

def load_configuration():
    if not os.path.exists(FILE_PATH_CONFIGURATION):
        print('File configuration not exists. You need run pmail.py config --create')
        return None

    configuration = configparser.ConfigParser()

    with open(FILE_PATH_CONFIGURATION, 'r') as conf_file:
        configuration.read_file(conf_file)
    
    return configuration

"""
    Command Function

    This section is reserved to functions that process input arguments
"""
def command_create_configuration(**kwargs):
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

def command_get_configuration(**kwargs):
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

def command_set_configuration(**kwargs):
    section, option, value = kwargs.get('opts').input
    configuration = kwargs.get('configuration')

    configuration[section][option] = value
    configuration.write(
        open(FILE_PATH_CONFIGURATION, 'w')
    )

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
    func=command_create_configuration
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
    func=command_get_configuration
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
    func=command_set_configuration
)

"""
    Main Function
"""
def main():
    global arguments

    configuration = load_configuration()

    opts = arguments.parse_args()
    opts.func(opts=opts, configuration=configuration)

if __name__ == '__main__':
    main()