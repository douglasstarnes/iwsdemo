from app import app, db, script_manager, constants
from flask.ext.script import Command, Option
from app.models import Client, TicketUser, ProductArea, Ticket
import getpass
from sqlalchemy.exc import IntegrityError
from app.security import user_datastore
import datetime
import random

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
        products = ['Billing', 'Claims', 'Policies', 'Reports']
        for product in products:
            p = ProductArea(name=product)
            db.session.add(p)
        admin = user_datastore.create_user(username='admin', password='adminP@55word', email='admin@example.com')
        admin_role = user_datastore.create_role(name='admin')
        user_datastore.add_role_to_user(admin, admin_role)

        developer1 = user_datastore.create_user(username='developer1', password='P@55word', email='developer1@example.com')
        developer2 = user_datastore.create_user(username='developer2', password='P@55word', email='developer2@example.com')
        db.session.commit()

        for i in range(12):
            ticket = Ticket(
                title='Sample Ticket {}'.format(i+1),
                description='Sample Description {}'.format(i+1),
                priority=[1,1,1,2,2,2,3,3,3,4,4,4][i],
                target = (datetime.datetime.now() + datetime.timedelta(days=random.randint(-2, 4))).date(),
                ticket_url = 'http://ticket{}.example.com'.format(i+1),
                client_id=(i%3) + 1,
                product_area_id=(i%4) + 1,
                assigned_to_id=(i%2) + 2
            )
            db.session.add(ticket)
            db.session.commit()

        print('example data inserted into db')

class CreateUserCommand(Command):
    def run(self):
        username = input('Username: ')
        password1 = getpass.getpass('Password: ')
        confim = getpass.getpass('Confirm password: ')

        if password == confirm:
            try:
                user_datastore.create_user(username=username, password=password)
                db.session.commit()
                print('user created')
            except IntegrityError:
                print('Username already in use')
        else:
            print('Passwords did not match')

script_manager.add_command('reset_database', ResetDatabaseCommand())
script_manager.add_command('populate_database', PopulateDatabaseCommand())
script_manager.add_command('create_user', CreateUserCommand())

if __name__ == '__main__':
    script_manager.run()
