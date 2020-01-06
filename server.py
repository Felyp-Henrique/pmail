import poplib
import getpass
import re

class POPServer():
    def __init__(self, host, username, password=None, port=None, ssl=False):
        if ssl:
            self.__server = poplib.POP3_SSL(
                host,
                port if port is not None else poplib.POP3_SSL_PORT,
            )
        else:
            self.__server = poplib.POP3(
                host,
                port if port is not None else poplib.POP3_PORT,
            )
        
        self.__server.user(username)

        self.__user_password = password

    def get_inbox(self):
        self.__server.pass_(self.__user_password or getpass.getpass())

        number_emails = len(self.__server.list()[1])

        inbox = []
        for i in range(1, number_emails + 1):
            email = self.__server.retr(i)[1]
            inbox.append(email)

        return inbox
    
    def __get_string_pattern_in_email(self, email, str_pattern):
        for email_str in email:
            compiled_pattern = re.compile(str_pattern)

            search = re.match(compiled_pattern, email_str)
            if search is not None:
                _, end_position = search.span()

                return search.string[end_position:].decode('utf-8').strip()

    def print_body_email(self, email):
        out = b"\n".join(email).decode('utf-8')
        print(out)

    def get_sender(self, email):
        return self.__get_string_pattern_in_email(email, br'^From:\s')

    def get_receiver(self, email):
        return self.__get_string_pattern_in_email(email, br'^To:\s')

    def get_subject(self, email):
        return self.__get_string_pattern_in_email(email, br'^Subject:\s')
    
    def get_date(self, email):
        return self.__get_string_pattern_in_email(email, br'^Date:\s')