from app import app, db, script_manager
from flask.ext.script import Command, Option
from app.models import Client

class ResetDatabaseCommand(Command):
    def run(self):
        confirm = input('All data will be deleted. Are you sure? (y/N)')
        if confirm.lower() == 'y':
            db.drop_all()
            db.create_all()
            print('database tables dropped and created')
        else:
            print('command cancelled')

class PopulateDatabaseCommand(Command):
    def run(self):
        clients = ['Client A', 'Client B', 'Client C']
        for client in clients:
            c = Client(name=client)
            db.session.add(c)
        db.session.commit()
        print('clients added')

script_manager.add_command('reset_database', ResetDatabaseCommand())
script_manager.add_command('populate_database', PopulateDatabaseCommand())

if __name__ == '__main__':
    script_manager.run()
