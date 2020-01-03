import time
import sys
import argparse

class Bootstrap():
    def __init__(self, app_name='pmail', description='Tool for e-mail backup'):
        self.app_name = app_name
        self.description = description

        self._commands = {}
        self._configuration = None
        self._connection_database = None
        self._time_init = time.strftime("%Y-%m-%d-%H-%M-%S")
        
        self._parser = argparse.ArgumentParser(self.app_name, description=self.description)

    def register_command(self, name, command_class):
        self._commands[name] = command_class
    
    def set_configuration(self, configuration):
        self._configuration = configuration

    def set_connection_database(self, connection):
        self._connection_database = connection

    def get_connection_database(self):
        return self._connection_database

    def get_time_init(self):
        return self._time_init

    def _prepare_argv_to_run_command(self):
        del(sys.argv[1]) # delete the name command of argv

    def _init_parser(self):
        name_commands = '; '.join([
            command_name for command_name, _ in self._commands.items()
        ])

        self._parser.add_argument('command', nargs='+', help=f"""
            \rcommand to run: { name_commands }
        """)

        opts = self._parser.parse_args()
        return opts

    def init(self):
        opts = self._init_parser()

        command = self._commands.get(opts.command[0], None)

        if command:
            self._prepare_argv_to_run_command()
            command().execute()
        else:
            self._parser.print_help()