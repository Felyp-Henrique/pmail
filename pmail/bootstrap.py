import time
import sys

class Bootstrap():
    def __init__(self):
        self._commands = {}
        self._configuration = None
        self._connection_database = None
        self._time_init = time.strftime("%Y-%m-%d %H-%M-%S")

    def register_command(self, name, command_class):
        self._commands[name] = command_class
    
    def set_configuration(self, configuration):
        self._configuration = configuration

    def get_connection_database(self):
        return self._connection_database

    def get_time_init(self):
        return self._time_init

    def init(self):
        name_command = sys.argv[1]
        
        command = self._commands[name_command]()
        command.execute()