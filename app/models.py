from app import db
from flask.ext.security import UserMixin, RoleMixin
from app import constants

roles_users = db.Table('roles_users',
    db.Column('ticket_user_id', db.Integer(), db.ForeignKey('ticket_user.id')),
    db.Column('ticket_role_id', db.Integer(), db.ForeignKey('ticket_role.id'))
)

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class ProductArea(db.Model):
    __tablename__ = 'product_area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class TicketUser(db.Model, UserMixin):
    __tablename__ = 'ticket_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    active = db.Column(db.Boolean())
    roles = db.relationship('TicketRole', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def is_admin(self):
        return self.has_role('admin')


class TicketRole(db.Model, RoleMixin):
    __tablename__ = 'ticket_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    priority = db.Column(db.Integer)
    target = db.Column(db.DateTime())
    ticket_url = db.Column(db.String(256))
    ticket_status = db.Column(db.Integer, default=constants.TICKET_STATUS_OPEN)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship(Client, backref=db.backref('tickets'))
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'))
    product_area = db.relationship(ProductArea, backref=db.backref('tickets'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('ticket_user.id'))
    assigned_to = db.relationship(TicketUser, backref=db.backref('tickets'))

    def decrease_priority(self):
        self.priority += 1
        db.session.add(self)
        db.session.commit()

    def increase_priority(self):
        self.priority -= 1
        db.session.add(self)
        db.session.commit()

    def get_status_message(self):
        return constants.STATUS_MESSAGES[self.ticket_status]
