import poplib
import re

class MailLoader():
    def __init__(self, host, port=0, ssl=False, username='', password=''):
        if not ssl:
            self.connection = poplib.POP3(
                host, port if port else poplib.POP3_PORT
            )
        else:
            self.connection = poplib.POP3_SSL(
                host, port if port else poplib.POP3_SSL_PORT
            )
        
        self.connection.user(username)
        self.connection.pass_(password)
    
    def get_mails(self):
        num_messages = len(self.connection.list()[1])

        return [self.connection.retr(i + 1)[1] for i in range(num_messages)]

    def get_mail_to(self, body_mail):
        field_necessary = re.compile(br'To: ')

        for line in body_mail:
            match = re.match(field_necessary, line)
            if match:
                _, end_match = match.span()
                return line.lower()[end_match:]

        return None

    def get_mail_from(self, body_mail):
        field_necessary = re.compile(br'From: ')

        for line in body_mail:
            match = re.match(field_necessary, line)

            if match:
                _, end_match = match.span()
                return line.lower()[end_match:]

        return None