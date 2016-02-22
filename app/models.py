from app import db

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class ProductArea(db.Model):
    __tablename__ = 'product_area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    priority = db.Column(db.Integer)
    target = db.Column(db.DateTime())
    ticket_url = db.Column(db.String(256))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship(Client, backref=db.backref('tickets'))
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'))
    product_area = db.relationship(ProductArea, backref=db.backref('tickets'))


