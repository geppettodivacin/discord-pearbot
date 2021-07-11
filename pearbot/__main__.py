import os
import sys

from .client import *

if __name__ == '__main__':
    token = (sys.argv[1] if len(sys.argv) >= 2
             else os.environ.get ('DISCORD_TOKEN'))

    client = Client ()
    client.run (token)
