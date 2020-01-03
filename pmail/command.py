from abc import abstractmethod
import argparse

class Command():
    help = '' # will used to displaying in help

    def __init__(self):
        self._parser = argparse.ArgumentParser()

    def add(self, name: str, *args, **kwargs) -> None:
        """Add new argument in parser

        see usage: https://docs.python.org/3.7/library/argparse.html#argumentparser-objects

        name        - str  - name of argument
        **kwargs    - dict - additional argument for add in argument parser
        """
        self._parser.add_argument(name, *args, **kwargs)

    @abstractmethod
    def add_arguments(self) -> None:
        """Use together with add() method to add arguments in child class
        """
        pass

    @abstractmethod
    def handle_arguments(self, opts: argparse.Namespace) -> None:
        """Will used to handle the arguments
        """
        pass

    def set_parser(self, parser):
        self._parser = parser

    def execute(self):
        self._parser.description = self.help
        
        self.add_arguments()

        args = self._parser.parse_args()

        self.handle_arguments(args)