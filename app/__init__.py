import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER_ROOT = ''

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object('config.Development')

db = SQLAlchemy(session_options={'autoflush': False})
db.app = app
db.init_app(app)

from app.models import *
from app.views import *
