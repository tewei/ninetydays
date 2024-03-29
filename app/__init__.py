from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

from app import models
from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app.mission import bp as mission_bp
app.register_blueprint(mission_bp)

from app.physio import bp as physio_bp
app.register_blueprint(physio_bp)

from app.wallet import bp as wallet_bp
app.register_blueprint(wallet_bp)

from app.monitor import bp as monitor_bp
app.register_blueprint(monitor_bp)