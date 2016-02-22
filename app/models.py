from app import db

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class ProductArea(db.Model):
    __tablename__ = 'product_area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class TicketUser(db.Model):
    __tablename__ = 'ticket_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))


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

    def decrease_priority(self):
        self.priority += 1
        db.session.add(self)
        db.session.commit()

    def increase_priority(self):
        self.priority -= 1
        db.session.add(self)
        db.session.commit()
