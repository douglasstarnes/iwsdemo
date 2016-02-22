from app import app, db, script_manager
from flask.ext.script import Command, Option
from app.models import Client, TicketUser
import getpass

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

class CreateUserCommand(Command):
    def run(self):
        username = input('Username: ')
        password1 = getpass.getpass('Password: ')
        password2 = getpass.getpass('Confirm password: ')

        if password1 == password2:
            user = TicketUser.query.filter_by(username=username).first()
            if user is None:
                ticket_user = TicketUser(username=username, password=password1)
                db.session.add(ticket_user)
                db.session.commit()
                print('added new user')
            else:
                print('username already exists')
        else:
            print('passwords did not match')
            
script_manager.add_command('reset_database', ResetDatabaseCommand())
script_manager.add_command('populate_database', PopulateDatabaseCommand())
script_manager.add_command('create_user', CreateUserCommand())

if __name__ == '__main__':
    script_manager.run()
