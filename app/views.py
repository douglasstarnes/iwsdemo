from app import app
from flask import render_template

@app.route('/new_ticket')
def new_ticket():
    return render_template('new_ticket.html')

@app.route('/')
def index():
    return 'hello flask'
