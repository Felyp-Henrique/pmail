from . import configuration
from . import database
import os

def get_connection_database(name):
    conf = configuration.Configuration()
    database_path = os.path.join(
        conf['database']['path'], name
    )

    return database.Connection(database_path)