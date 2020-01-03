from configparser import ConfigParser
import pathlib
import os
from . import database

HOME = pathlib.Path.home()
DEFAULT_CONFIGURATION = os.path.join(HOME, '.pmail')

class Configuration(ConfigParser):
    def __init__(self, file=DEFAULT_CONFIGURATION, **kwargs):
        super().__init__(**kwargs)
        self.file = file

    def read_config(self):
        with open(self.file, 'r') as file_conf:
            self.read_file(file_conf)

    def save(self):
        with open(self.file, 'w') as file_conf:
            self.write(file_conf)
    
    @classmethod
    def create_config(self, file=DEFAULT_CONFIGURATION):
        if os.path.exists(file):
            return
        
        os.mknod(file)
        conf = Configuration()
        
        conf_str = """
            \r[backup]
            \rpath=%s
            \rname=backup
            \rfrequent_day=1
        """ % database.DEFAULT_DATABASE

        conf.read_string(conf_str)

        with open(file, 'w') as file_conf:
            conf.write(file_conf)