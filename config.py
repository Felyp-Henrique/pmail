from configparser import ConfigParser
import pathlib
import os
import db

HOME = pathlib.Path.home()
DEFAULT_CONFIGURATION = os.path.join(HOME, '.pmail')

class Configuration(ConfigParser):
    def __init__(self, file=DEFAULT_CONFIGURATION, **kwargs):
        super().__init__(**kwargs)
        self.file = file

    def read_config(self):
        self.read_file(self.file)

    def save(self):
        with open(self.file, 'w') as file_conf:
            self.write(file_conf)
    
    @classmethod
    def create_config(self, file=DEFAULT_CONFIGURATION):
        if os.path.exists(file):
            return
        
        os.mknod(file)
        conf = Configuration()
        conf.add_section('database')
        conf['database']['sqlite_db_path'] = db.DEFAULT_DATABASE

        with open(file, 'w') as file_conf:
            conf.write(file_conf)