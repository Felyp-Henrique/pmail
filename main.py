from pmail import bootstrap, configuration

import commands

def main():
    app = bootstrap.Bootstrap()
    configuration.Configuration.create_config()

    conf = configuration.Configuration()
    conf.read_config()

    app.set_configuration(conf)
    app.register_command('list_email', commands.ListInboxAccountCommand)

    app.init()

if __name__ == '__main__':
    main()