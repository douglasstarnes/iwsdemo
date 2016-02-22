from app import app
from flask import render_template, request
from app.models import Client, ProductArea

@app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    if request.method == 'GET':
        clients = Client.query.all()
        products = ProductArea.query.all()
        return render_template('new_ticket.html', clients=clients, products=products)
    else:
        title = request.form['title']
        description = request.form['description']
        top_queue = request.form['top_queue']
        target_date = request.form['target_date_input']
        client = request.form['client']
        product_area = request.form['product_area']
        return '{}<br/>{}<br/>{}<br/>{}<br/>{}<br/>{}<br/>'.format(
            title, description, top_queue, target_date, client, product_area
        )

@app.route('/')
def index():
    return 'hello flask'
