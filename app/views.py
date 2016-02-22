from app import app, db
from flask import render_template, request
from app.models import Client, ProductArea, Ticket
import datetime, time, re

def parse_date(date_string):
    pattern = '\w{3}\s\w{3}\s\d{2}\s\d{4}'
    match = re.search(pattern, date_string)
    ts = time.strptime(match.group(0), '%a %b %d %Y')
    return datetime.datetime.fromtimestamp(time.mktime(ts))

@app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    if request.method == 'GET':
        clients = Client.query.all()
        products = ProductArea.query.all()
        return render_template('new_ticket.html', clients=clients, products=products)
    else:
        title = request.form['title']
        description = request.form['description']
        top_queue = False
        if request.form.get('top_queue'):
            top_queue = True if request.form['top_queue'] else False
        target_date = request.form['target_date']
        client_id = request.form['client']
        product_area_id = request.form['product_area']

        client = Client.query.get(int(client_id))
        product_area = ProductArea.query.get(int(product_area_id))

        if top_queue == True:
            for ticket in client.tickets:
                ticket.decrease_priority()



        ticket = Ticket(
            title=title,
            description=description,
            priority=1 if top_queue == True else len(client.tickets)+1,
            target=parse_date(target_date),
            ticket_url='',
            client = client,
            product_area=product_area
        )
        db.session.add(ticket)
        db.session.commit()

        return target_date

@app.route('/tickets')
def tickets():
    clients = Client.query.all()
    return render_template('tickets.html', clients=clients)

@app.route('/')
def index():
    return 'hello flask'
