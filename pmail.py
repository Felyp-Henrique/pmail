import core
import server
import db
from email import EmailTable
import utils

class App(core.AppAbstract):
    def add_arguments(self):
        self.add_argument('--username', type=str, help='email of user as: username@hostname.com')
        self.add_argument('--password', type=str, help='password of user')

    def run_when_username_pass_as_input(self, opts):
        print('Backup from only username')

        conf_server = self.configuration.get('server')
        
        srv = server.POPServer(
            host=conf_server.get('host', 'localhost'),
            username=opts.username,
            password=opts.password,
            port=conf_server.get('port', server.poplib.POP3_PORT),
            ssl=conf_server.get('ssl', False),
        )

        inbox = srv.get_inbox()
        
        path_db, name_db = utils.get_path_and_name_db(self)

        email_table = EmailTable()
        email_table.connection = db.DataBaseConnection(path_db, name_db)
        email_table.create_table()

        for email in inbox:
            email_table['date'] = srv.get_date(email)
            email_table['subject'] = srv.get_subject(email)
            email_table['sender'] = srv.get_sender(email)
            email_table['receiver'] = srv.get_receiver(email)

            body_protocol = "\n".join([line.decode('utf-8') for line in email])
            email_table['body_protocol'] = body_protocol

            email_table.save()

    def run_with_list_users(self):
        print('Backup multiple users')

        conf_server = self.configuration.get('server')
        conf_users = self.configuration.get('users')
        
        path_db, name_db = utils.get_path_and_name_db(self)

        email_table = EmailTable()
        email_table.connection = db.DataBaseConnection(path_db, name_db)
        email_table.create_table()

        for username, password in conf_users.items():
            srv = server.POPServer(
                host=conf_server.get('host', 'localhost'),
                username=username,
                password=password,
                port=conf_server.get('port', server.poplib.POP3_PORT),
                ssl=conf_server.get('ssl', False),
            )

            inbox = srv.get_inbox()

            for email in inbox:
                email_table['date'] = srv.get_date(email)
                email_table['subject'] = srv.get_subject(email)
                email_table['sender'] = srv.get_sender(email)
                email_table['receiver'] = srv.get_receiver(email)

                body_protocol = "\n".join([line.decode('utf-8') for line in email])
                email_table['body_protocol'] = body_protocol

                email_table.save()

    def handle_input(self, opts):
        if opts.username is not None:
            self.run_when_username_pass_as_input(opts)
            
            return # exit the command
        
        self.run_with_list_users()

if __name__ == "__main__":
    App.create_configuration() # create configuration if not exists

    app = App(app_name='PMail', description='E-Mail Buckupper')
    app.load_configuration()
    app.loop()