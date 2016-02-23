from flask.ext.security import Security, SQLAlchemyUserDatastore
from app.models import TicketUser, TicketRole
from app import app, db

user_datastore = SQLAlchemyUserDatastore(db, TicketUser, TicketRole)
security = Security(app, user_datastore)
