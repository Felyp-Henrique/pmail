#!/usr/bin/env python3
"""
    POP Module

    This module has the definition for handle the inbox POP3
"""
import poplib
from collections.abc import Generator
from .abc import EmailClient


class POP3(EmailClient):
    """
        POP3

        This class is as a proxy that encapsulates the
        class POP3 and POP3_SSL from module poplib.
    """
    def __init__(self, host: str = 'localhost') -> None:
        self.username = ''
        self.password = ''
        self.host = host
        self.port = poplib.POP3_PORT
        self.timeout = 30
        self._using_ssl = False
        self._server = None
        self._is_connected = False
        self._keyfile = None
        self._certfile = None

    @property
    def ssl_enable(self) -> bool:
        """Return if SSL is enable"""
        return self._using_ssl

    @ssl_enable.setter
    def ssl_enable(self, enable: bool = False):
        """
            Switch state between enable/disable SSL.
            
            If the port is equals POP3_PORT constant or
            POP3_SSL_PORT, then, the class switch the port automatically.
            Else, means that user is use different value port than common, then
            the class not switch the port automatically.
        """
        self._using_ssl = enable
        if enable and self._port == poplib.POP3_PORT:
            self._port = poplib.POP3_SSL_PORT
        elif self._port == poplib.POP3_SSL_PORT:
            self._port = poplib.POP3_SSL_PORT

    def ssl_keyfile(self, file_) -> None:
        """Set the SSL Key File"""
        self._keyfile = file_

    def ssl_certfile(self, file_) -> None:
        """Set the certification file SSL"""
        self._certfile = file_

    def is_connected(self) -> bool:
        """Return if is connected"""
        return self._is_connected

    def messages(self) -> Generator:
        """Return the Generator of inbox"""
        amount_email = len(self._server.list()[1])
        return (b"\n".join(self._server.retr(i + 1)[1]) for i in range(amount_email))

    def connect(self) -> None:
        """Initialize the connection with server"""
        if self._is_connected:
            return

        if not self._using_ssl:
            self._server = poplib.POP3(
                self.host,
                self.port,
                self.timeout
            )
        else:
            # Waning: this implementation was not tested
            self._server = poplib.POP3_SSL(
                self.host,
                self.port,
                self._keyfile,
                self._certfile,
                self.timeout
            )
        self._server.user(self.username)
        self._server.pass_(self.password)
        self._is_connected = True

    def reconnect(self) -> None:
        """First disconnect after connect again"""
        self.disconnect()
        self.connect()
        self._is_connected = True

    def disconnect(self) -> None:
        """Commit changes and close connection with server"""
        self._server.quit()
        self._server.close()
        self._is_connected = False

    def __repr__(self):
        return "POP3(%r)" % self.host
