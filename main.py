from pmail import bootstrap, configuration, database

import commands
import os

def main():
    app = bootstrap.Bootstrap()
    configuration.Configuration.create_config()

    conf = configuration.Configuration()
    conf.read_config()

    app.set_configuration(conf)

    db_path = "%s%s-%s.sqlite3" % (
        conf['backup']['path'],
        app.get_time_init(),
        conf['backup']['name']
    )

    db = database.Connection()
    print(db_path)
    db.connect(db_path)

    app.set_connection_database(db)

    app.register_command('inbox', commands.ListInboxAccountCommand)

    app.init()

    db.close_connection()

if __name__ == '__main__':
    main()