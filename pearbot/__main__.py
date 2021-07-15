import os
import sqlite3
import sys

from contextlib import closing

from .bot import *

from . import database

if __name__ == '__main__':
    token = (sys.argv[1] if len(sys.argv) >= 2
             else os.environ.get ('DISCORD_TOKEN'))

    with closing(database.Connection(sqlite3.connect(':memory:'))) as connection:
        client = create_bot (connection, '!')
        client.run (token)
