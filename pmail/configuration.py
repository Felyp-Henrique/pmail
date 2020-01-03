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
        
        list_conf = 'database:path file_backup:name,sufix'.split()
        for section_fields in list_conf:
            section, fields = section_fields.split(':')

            conf.add_section(section)
            conf[section] = { field: 'None' for field in fields.split(',') }

        with open(file, 'w') as file_conf:
            conf.write(file_conf)