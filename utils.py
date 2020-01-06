import db

def get_path_and_name_db(app):
    conf_backup = app.configuration.get('backup')

    path = conf_backup.get('path', db.DEFAUTL_PATH_DATABASE)
    name = f"{ app.time_init } { conf_backup.get('name') }.sqlite3"

    return path, name
