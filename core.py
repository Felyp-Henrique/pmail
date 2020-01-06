import argparse
import poplib
import configparser
import os
import pathlib
import abc
import datetime
import time

import server

DEFAULT_CONFIGURATION = os.path.join(pathlib.Path.home(), '.pmail')

class AppAbstract(abc.ABC):
    configuration = {
        'backup': {
            'path': pathlib.Path.home(),
            'name': 'backup',
            'repeat_on_time': '24', # wait one day to repeat
        },

        'server': {
            'host': 'locahost',
            'port': poplib.POP3_PORT,
            'ssl': False,
        },

        'users': {},
    }

    def __init__(self, app_name, description):
        self.__parser = argparse.ArgumentParser(
            app_name, description=description
        )

        now = datetime.datetime.now()
        self.time_init = now.strftime("%Y-%m-%d %H-%M-%S")

        self.__conf_file = configparser.ConfigParser()
        self.__conf_file.read_dict(self.configuration)
    
    @classmethod
    def create_configuration(self, path=DEFAULT_CONFIGURATION):
        if os.path.exists(path): # if exists not need create
            return

        conf = configparser.ConfigParser()
        conf.read_dict(AppAbstract.configuration)

        with open(path, 'w') as conf_file:
            conf.write(conf_file)

    def load_configuration(self, path=DEFAULT_CONFIGURATION):
        with open(path, 'r') as conf_file:
            self.__conf_file.read_string(conf_file.read())

        # update dict configuration
        for option, value in self.__conf_file.items():
            if option == 'ssl':
                value = True if value == 'True' else False
        
            self.configuration[option] = value
    
    def save_configuration(self, path=DEFAULT_CONFIGURATION):
        with open(path, 'w') as conf_file:
            conf.write(self.configuration)

    def add_argument(self, name, *args, **kwargs):
        self.__parser.add_argument(name, *args, **kwargs)
    
    def add_argument(self, name, *args, **kwargs):
        self.__parser.add_argument(name, *args, **kwargs)

    @abc.abstractmethod
    def add_arguments(self):
        pass

    @abc.abstractmethod
    def handle_input(self, opts: argparse.Namespace):
        pass

    def execute(self):
        self.add_arguments()

        opts = self.__parser.parse_args()

        self.handle_input(opts)
    
    def loop(self):
        conf_backup = self.configuration.get('backup')
        repeat_on_time = conf_backup.get('repeat_on_time')

        while True:
            os.system('cls | clear')

            now = datetime.datetime.now()
            print(now.strftime('PMail Backup: %H:%M:%S'))
            
            if now.strftime('%H') == repeat_on_time:
                print('Run...')
                
                self.execute()

                print('Done!')
            
            time.sleep(1)