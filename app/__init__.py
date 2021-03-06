from flask import *
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import *

db = SQLAlchemy()

def create_app():
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config['APP'] = 'app'
  app.config['SECRET_KEY'] = 'secret-key-goes-here'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false
  app.config["JSON_AS_ASCII"] = False

  db.init_app(app)
  migrate = Migrate(app, db)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  from .models import User

  @login_manager.user_loader
  def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app
