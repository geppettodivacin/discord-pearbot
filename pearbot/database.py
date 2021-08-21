import sqlite3
from collections import namedtuple

_tables = [
    ('Users', ['Id STRING PRIMARY KEY', 'Guild BIGINT'])
]

User = namedtuple('User', ['id', 'guild'])

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

    def users(self, guild):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM Users WHERE Guild=?', (guild,))
        return map(User._make, cursor.fetchall())

    def unpaired_users(self, guild):
        cursor = self.connection.cursor()
        # TODO: Add a joined query to the pairing table
        cursor.execute('SELECT * FROM Users WHERE Guild=?', (guild,))
        return map(User._make, cursor.fetchall())

class TransactionManager(object):
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        return Transaction (self.connection.__enter__())

    def __exit__(self, *args, **kwargs):
        self.connection.__exit__(*args, **kwargs)
