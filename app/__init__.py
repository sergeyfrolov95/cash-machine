import os
from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER_ROOT = ''

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object('config.Development')

#babel = Babel(app)

# Debug toolbar
# from flask_debugtoolbar import DebugToolbarExtension
# app.debug = True
# toolbar = DebugToolbarExtension(app)

#db = SQLAlchemy(session_options={'autoflush': False})
#db.app = app
#db.init_app(app)

#from app.models import *
from app.views import *

#login_manager = LoginManager()
#login_manager.init_app(app)


#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.filter_by(id=user_id).first()
