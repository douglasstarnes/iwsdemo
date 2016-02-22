from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from app.config import DevelopmentConfig
import os

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
script_manager = Manager(app)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)

from app import views
