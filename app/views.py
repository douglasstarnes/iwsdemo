from app import app, db, api, constants
from flask import render_template, request, flash, redirect, url_for
from app.models import Client, ProductArea, Ticket, TicketUser, TicketRole
import datetime, time, re
from flask_restful import Resource
from flask.ext.security import login_required, roles_required, current_user
import string
import random
from app.security import user_datastore

def parse_date(date_string):
    pattern = '\w{3}\s\w{3}\s\d{2}\s\d{4}'
    match = re.search(pattern, date_string)
    ts = time.strptime(match.group(0), '%a %b %d %Y')
    return datetime.datetime.fromtimestamp(time.mktime(ts))

def gen_password(l):
    haystack = string.ascii_letters + string.digits + '!@#$%^&*()'
    return ''.join([random.choice(haystack) for _ in range(l)])

@app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    if request.method == 'GET':
        clients = Client.query.all()
        products = ProductArea.query.all()
        users = TicketUser.query.all()
        return render_template('new_ticket.html', clients=clients, products=products, users=users)
    else:
        title = request.form['title']
        description = request.form['description']
        top_queue = False
        if request.form.get('top_queue'):
            top_queue = True if request.form['top_queue'].lower() == 'on' else False
        target_date = request.form['target_date']
        client_id = request.form['client']
        product_area_id = request.form['product_area']
        ticket_url = request.form['ticket_url']
        user_id = request.form['assigned_to']

        client = Client.query.get(int(client_id))
        product_area = ProductArea.query.get(int(product_area_id))
        user = TicketUser.query.get(int(user_id))

        if top_queue == True:
            for ticket in client.tickets:
                ticket.decrease_priority()

        ticket = Ticket(
            title=title,
            description=description,
            priority=1 if top_queue == True else len(client.tickets)+1,
            target=parse_date(target_date),
            ticket_url=ticket_url,
            client = client,
            product_area=product_area,
            assigned_to = user
        )
        db.session.add(ticket)
        db.session.commit()

        ticket.add_log(constants.TICKET_LOG_TYPE_STATUS_CHANGE)

        return redirect(url_for('tickets'))

@app.route('/my_tickets/<int:ticket_id>')
@app.route('/my_tickets')
@login_required
def my_tickets(ticket_id=None):
    if ticket_id == None:
        tickets = current_user.tickets
        grouped_tickets = {}
        for ticket in tickets:
            if not ticket.client.name in grouped_tickets.keys():
                grouped_tickets[ticket.client.name] = []
            grouped_tickets[ticket.client.name].append(ticket)
        for k in grouped_tickets.keys():
            grouped_tickets[k] = sorted(grouped_tickets[k], key=lambda x: x.priority)
        return render_template('my_tickets.html', grouped_tickets=grouped_tickets, client_names=[client.name for client in Client.query.order_by(Client.name).all()])
    else:
        ticket = Ticket.query.get(ticket_id)
        if ticket is not None and ticket.assigned_to == current_user:
            return render_template('ticket_details.html', ticket=ticket, constants=constants)
        else:
            flash('You can only access tickets that have been assigned to you')
            return redirect(url_for('my_tickets'))

@app.route('/create_user', methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    else:
        username = request.form['username']
        email = request.form['email']
        generate_password = False
        if request.form.get('generate_password'):
            generate_password = True if request.form['generate_password'].lower() == 'on' else False
        if generate_password:
            password = confirm = gen_password(12)
        else:
            password = request.form['password']
            confirm = request.form['confirm']
        if len(password) < app.config['MIN_PASSWORD_LENGTH'] or len(confirm) < app.config['MIN_PASSWORD_LENGTH']:
            flash('Password must be at least {} characters'.format(app.config['MIN_PASSWORD_LENGTH']))
            return redirect(url_for('create_user'))
        if not password == confirm:
            flash('Passwords did not match each other, please try again')
            return redirect(url_for('create_user'))
        try:
            user_datastore.create_user(email=email, password=password, username=username)
            db.session.commit()
            if generate_password:
                flash('User created with password: {}'.format(password))
            else:
                flash('User created')
            return redirect(url_for('list_users'))
        except IntegrityError:
            flash('Email is already in use')
            return redirect(url_for('create_user'))

@app.route('/list_users')
@roles_required('admin')
@login_required
def list_users():
    users = TicketUser.query.all()
    return render_template('list_users.html', users=users)

@app.route('/user_details/<int:user_id>')
@roles_required('admin')
@login_required
def user_details(user_id):
    user = TicketUser.query.get(user_id)
    if user is None:
        flash('User could not be found')
        return redirect(url_for('list_users'))
    else:
        return render_template('user_details.html', user=user)

@app.route('/toggle_user_active/<int:user_id>')
@roles_required('admin')
@login_required
def toggle_user_active(user_id):
    if not current_user.id == user_id: #don't want users to deactivate their own accounts
        user = TicketUser.query.get(user_id)
        if user is not None:
            user.active = not user.active
            db.session.add(user)
            db.session.commit()
    return redirect(url_for('user_details', user_id=user_id))

@app.route('/manage_roles/<int:user_id>', methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def manage_roles(user_id):
    user = TicketUser.query.get(user_id)
    if user is not None:
        all_roles = [role.name for role in TicketRole.query.all()]
        if request.method == 'GET':
            active_roles = [role for role in all_roles if user.has_role(role)]
            inactive_roles = list(set(all_roles).difference(set(active_roles)))
            return render_template('manage_roles.html', active_roles=active_roles, inactive_roles=inactive_roles, user=user)
        else:
            for role in all_roles:
                if request.form.get('role_' + role):
                    if not user.has_role(role):
                        user_datastore.add_role_to_user(user, role)
                else:
                    if user.has_role(role):
                        user_datastore.remove_role_from_user(user, role)
            db.session.commit()
            return redirect(url_for('user_details', user_id=user_id))
    return redirect(url_for('list_users'))

@app.route('/ticket_next/<int:ticket_id>')
@login_required
def ticket_next(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket is not None and ticket.assigned_to == current_user:
        if ticket.ticket_status >= 0:
            next_status = ticket.get_status_meta()['next_status']
            ticket.ticket_status = next_status
            db.session.add(ticket)
            db.session.commit()
            ticket.add_log(constants.TICKET_LOG_TYPE_STATUS_CHANGE)
        return redirect(url_for('my_tickets', ticket_id=ticket_id))
    else:
        flash('You can only access tickets assigned to you')
        return redirect(url_for('my_tickets'))

@app.route('/tickets/<int:ticket_id>')
@app.route('/tickets')
@roles_required('admin')
@login_required
def tickets(ticket_id=None):
    if ticket_id is None:
        clients = Client.query.all()
        return render_template('tickets.html', clients=clients)
    else:
        ticket = Ticket.query.get(ticket_id)
        if ticket is not None:
            return render_template('ticket_details.html', ticket=ticket, constants=constants)
        else:
            flash('Ticket could not be found')
            return redirect(url_for('tickets'))

@app.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def edit_ticket(ticket_id):
    if request.method == 'GET':
        ticket = Ticket.query.get(ticket_id)
        if ticket is not None:
            clients = Client.query.all()
            products = ProductArea.query.all()
            users = TicketUser.query.all()
            return render_template('edit_ticket.html', ticket=ticket, clients=clients, products=products, users=users)
        else:
            flash('Ticket could not be found')
            return redirect(url_for('tickets'))
    else:
        title = request.form['title']
        description = request.form['description']
        target_date = request.form['target_date']
        client_id = request.form['client']
        product_area_id = request.form['product_area']
        ticket_url = request.form['ticket_url']
        user_id = request.form['assigned_to']

        client = Client.query.get(int(client_id))
        product_area = ProductArea.query.get(int(product_area_id))
        user = TicketUser.query.get(int(user_id))

        ticket = Ticket.query.get(ticket_id)
        if ticket is not None:
            ticket.title = title
            ticket.description = description
            ticket.target=parse_date(target_date)
            ticket.client = client
            ticket.product_area = product_area
            ticket.assigned_to = user
            ticket.ticket_url = ticket_url

            db.session.add(ticket)
            db.session.commit()

            ticket.add_log(message_content='Edited ticket')

            return redirect(url_for('tickets', ticket_id=ticket_id))


@app.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    ticket = Ticket.query.get(int(request.form['ticket_id']))
    if ticket is not None and (ticket.assigned_to == current_user or current_user.is_admin() == True):
        ticket.add_log(message_content=request.form['log_message'])
        return redirect(url_for('my_tickets', ticket_id=ticket.id))
    else:
        return redirect(url_for('my_tickets'))

@app.route('/forbidden')
def forbidden():
    return render_template('forbidden.html')


@app.route('/dashboard')
@roles_required('admin')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    return render_template('index.html')

class TicketsApi(Resource):
    def get(self, client_id):
        if int(client_id) > 0:
            tickets = Ticket.query.filter_by(client_id=client_id)
        else:
            tickets = Ticket.query.all()
        return [
            {
                'id': ticket.id,
                'client': ticket.client.name,
                'title': ticket.title,
                'description': ticket.description,
                'target': ticket.target.strftime('%b. %d, %Y'),
                'ticket_url': ticket.ticket_url,
                'product_area': ticket.product_area.name,
                'priority': ticket.priority,
                'assigned_to': ticket.assigned_to.username,
                'overdue': ticket.is_overdue()
            }
            for ticket in tickets
        ]
