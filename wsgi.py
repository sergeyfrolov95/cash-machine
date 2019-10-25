import sys

sys.path.insert(0, '/home/sergey/dev/cash-machine')

from app import app as application, db as database
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# Migration
migrate = Migrate(application, database)

# Initialize a manager for commands
manager = Manager(application)
manager.add_command('db', MigrateCommand)


# Run server
if __name__ == '__main__':
    manager.run()
