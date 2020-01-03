import getpass

from pmail import command, mail

class ListInboxAccountCommand(command.Command):
    help = 'List Inbox from an account'

    def add_arguments(self):
        self.add('email', type=str, help='email from user to get the list of Inbox')
        self.add('host_pop', type=str, help='the email server')
        self.add('--port', type=int, help='port server', default=0)
        self.add('--ssl', action='store_true', help='flagging to use SSL security')
    
    def handle_arguments(self, opts):
        password = getpass.getpass()
        email = opts.email.split('=')[1]
        host = opts.host_pop.split('=')[1]

        email = mail.MailLoader(
            host,
            opts.port,
            opts.ssl,
            email,
            password
        )

        for e in email.get_mails():
            output = "From: %s\t To: %s"% (
                email.get_mail_from(e).decode('utf-8'),
                email.get_mail_to(e).decode('utf-8'),
            )

            print(output)