import sqlite3
import pathlib
import os
from inspect import getmembers, ismethod

HOME = str(pathlib.Path.home())
DEFAULT_DATABASE = os.path.join(HOME, '.pmail.sqlite3')

class Connection():
    def __init__(self, db=DEFAULT_DATABASE):
        self.db = sqlite3.connect(db)

    def run_and_get_result(self, sql, *args):
        cur = self.db.cursor()
        cur.execute(sql, args)

        result = cur.fetchall()
        cur.close()

        return result
    
    def run_and_get_first_result(self, sql, *args):
        result = self.run_and_get_result(sql, *args)

        if len(result) > 0:
            return result[0]

        return None
    
    def run(self, sql, *args):
        cur = self.db.cursor()
        cur.execute(sql, args)
        self.db.commit()
        cur.close()
    
    def close_connection(self):
        self.db.close()

    @classmethod
    def get_connection(self):
        return Connection()

class Field():
    def __init__(self, type_field=str, name='', value='', **kwargs):
        self.type_field = type_field
        self.name = name
        self.value = value
        self.primary_key = kwargs.get('primary_key', False)

    def get_create_format(self):
        more_details = ''
        if self.primary_key:
            more_details += 'PRIMARY KEY '

        if self.value:
            more_details += f'DEFAULT { self.value } '

        return f'{ self.name } { self.get_type_field() } { more_details }'

    def get_type_field(self):
        if self.type_field is str:
            return 'TEXT'
        
        if self.type_field is int:
            return 'INTEGER'
    
    def get_value(self):
        if self.type_field is str:
            return f"'{ self.value }'"
        
        return self.value

class Model():
    SQL_CREATE_FORMAT = """
        CREATE TABLE IF NOT EXISTS %s (
            %s
        )
    """

    SQL_SELECT_FORMAT = """
        SELECT * FROM %s %s
    """

    SQL_INSERT_FORMAT = """
        INSERT INTO %s (%s) VALUES (%s)
    """

    SQL_UPDATE_FORMAT = """
        UPDATE %s SET %s WHERE %s
    """

    def __init__(self):
        # define the name of table with name of class
        class_name = self.__class__.__name__.lower()
        self.table = class_name
        self.register_inserted = False
        self.connection = Connection.get_connection()

    def get_fields(self):
        return [
            getattr(self, field) for field, _ in getmembers(self)
            if isinstance(getattr(self, field), Field)
        ]

    def create_table_if_not_exists(self):
        table_name = self.__class__.__name__.lower()
        connection = Connection.get_connection()

        fields = ','.join([
            field.get_create_format() for field in self.get_fields()
        ])

        sql = self.SQL_CREATE_FORMAT % (table_name, fields)

        connection.run(sql)

    def get_all(self):
        sql = self.SQL_SELECT_FORMAT % (self.table, '')
        return self.connection.run_and_get_result(sql)

    @classmethod
    def get(self, **kwargs):
        table_name = self.__name__.lower()
        connection = Connection.get_connection()

        where_args = 'WHERE ' + ' AND '.join([
            '%s = %s' % field_and_value for field_and_value in kwargs.items()
        ])

        sql = self.SQL_SELECT_FORMAT % (table_name, where_args)
        register = connection.run_and_get_first_result(sql)

        return self.set_result_sql_into_object_model(register)

    @classmethod
    def set_result_sql_into_object_model(self, result_sql):
        # get fields objects
        fields = [
            getattr(self, field) for field, value in getmembers(self)
            if isinstance(getattr(self, field), Field)
        ]

        result = self()
        result.register_inserted = True

        for i, old_field_value in enumerate(fields):
            value_column_result = result_sql[i]
            
            new_value_field = Field()
            new_value_field.type_field = old_field_value.type_field
            new_value_field.name = old_field_value.name
            new_value_field.value = value_column_result
            new_value_field.primary_key = old_field_value.primary_key

            setattr(result, old_field_value.name, new_value_field)

        return result

    def save(self):
        fields = [field.name for field in self.get_fields()]
        values = [str(field.get_value()) for field in self.get_fields()]

        # if do not has insert in table, insert, else, update
        if self.register_inserted:
            fields_values = ','.join([
                f'{ field } = { value }' for field, value in list(zip(fields, values))
            ])

            sql = self.SQL_UPDATE_FORMAT % (
                self.table,
                fields_values,
                getattr(self, 'id') # the class Model expect id field in class child
            )
        else:
            sql = self.SQL_INSERT_FORMAT % (
                self.table, ','.join(fields), ','.join(values)
            )

        self.connection.run(sql)
        self.register_inserted = True