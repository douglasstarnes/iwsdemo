from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from app.config import DevelopmentConfig
import os
from flask_restful import Api
from flask.ext.security import Security


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
script_manager = Manager(app)
api = Api(app)

from app import views
from app import security

api.add_resource(views.TicketsApi, '/api/tickets/<client_id>')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)
