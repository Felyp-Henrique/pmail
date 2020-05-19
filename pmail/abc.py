#!/usr/bin/env python3
"""
    ABC

    This class has the interface to write class for
    interact with email server and more
"""
from abc import ABC, abstractmethod
from collections.abc import Generator


class EmailClient(ABC):
    """Interface for email client"""
    
    @abstractmethod
    def messages(self) -> Generator:
        """Iterable with messages"""

    @abstractmethod
    def connect(self) -> None:
        """Connect with server"""

    @abstractmethod
    def reconnect(self) -> None:
        """Reconnect with server"""

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect with server"""

