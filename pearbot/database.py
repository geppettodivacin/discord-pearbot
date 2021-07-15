import sqlite3

_tables = [
    ('Users', ['Name STRING PRIMARY KEY', 'Guild BIGINT'])
]

class Connection(object):
    def __init__(self, connection):
        self.connection = connection
        with connection:
            [connection.execute(
                    f'CREATE TABLE IF NOT EXISTS {table_name} ({",".join(columns)})')
                for (table_name, columns) in _tables]

    def close(self):
        return self.connection.close()

    def transaction(self):
        return TransactionManager(self.connection)

class Transaction(object):
    def __init__(self, connection):
        self.connection = connection

    def register_user(self, user, guild):
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO Users VALUES (?, ?)', (user, guild))

    def users(self):
        cursor = self.connection.cursor()
        return cursor.execute('SELECT * FROM Users').fetchall()

class TransactionManager(object):
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        return Transaction (self.connection.__enter__())

    def __exit__(self, *args, **kwargs):
        self.connection.__exit__(*args, **kwargs)
