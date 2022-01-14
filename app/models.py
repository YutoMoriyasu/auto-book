from flask_login import UserMixin
from sqlalchemy_utils import UUIDType
import uuid
from . import db

class User(UserMixin, db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  name = db.Column(db.String(1000))
  created_at = db.Column(db.DATETIME)

class Post(db.Model):
  __tablename__ = 'post'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
  title = db.Column(db.String(1000))
  url = db.Column(db.String(1000))
  created_at = db.Column(db.DATETIME)

class Group(db.model):
  __tablename__ = 'group'
  id = db.Column(UUIDType(binary=False), primary_key=True, default=str(uuid.uuid4()))
  name = db.Column(db.String(1000))