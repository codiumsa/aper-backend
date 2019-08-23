from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS 

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

from .db import db_session, Base
from flask_migrate import Migrate

migrate = Migrate(app, Base)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import aper.auth
import aper.views
