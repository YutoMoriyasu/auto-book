import os

from flask import Flask, render_template, request, redirect
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///user.db')  # user.db というデータベースを使うという宣言です
Base = declarative_base()  # データベースのテーブルの親です

class User(Base):  # PythonではUserというクラスのインスタンスとしてデータを扱います
  __tablename__ = 'users'  # テーブル名は users です
  user_id = Column(Integer, primary_key=True, unique=True)  # 整数型のid をprimary_key として、被らないようにします
  email = Column(String)  # 文字列の emailというデータを作ります
  name = Column(String)  # 文字列の nameというデータを使います
  def __repr__(self):
      return "User<{}, {}, {}>".format(self.user_id, self.email, self.name)

Base.metadata.create_all(engine)  # 実際にデータベースを構築します
SessionMaker = sessionmaker(bind=engine)  # Pythonとデータベースの経路です
session = SessionMaker()  # 経路を実際に作成しました

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
  )

  login_manager = LoginManager()
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))
  
  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # トップページ
  @app.route('/')
  @login_required
  def index():
    # TODO ユーザーに対して、登録しているグループの情報を取得する処理を記述する
    test = 'テンプレートエンジンのテスト'
    return render_template('index.html', test=test)

  # 個別のグループページ
  @app.route('/groups/<group_id>') # /groups/<group_id>にアクセスしたとき
  @login_required
  def group(group_id):
    # TODO 個別のグループの情報を取得する処理を記述する
    return render_template('group.html', group_id=group_id) # group.htmlに変数group_idを渡す
  
  # サインアップページ
  @app.route('/signup', methods=['GET','POST'])
  def signup():
    if request.method == 'POST':
      username = request.form.get('username')
      email = request.form.get('email')
      # Userのインスタンスを作成
      user = User(name = username, email = email)
      session.add(user)
      session.commit()
      return redirect('/login')
    else:
      return render_template('signup.html')

  # ログイン画面
  @app.route('/login', methods=['GET','POST'])
  def login():
    if request.method == 'POST':
      username = request.form.get('username')
      email = request.form.get('email') 
      user = session.query(User).filter(User.name == username).all()
      for user in user:
        if user.email == email:
          return render_template('index.html')
    else:
      return render_template('login.html')
  
  # ログアウト
  @app.route('/logout')
  @login_required
  def logout():
    logout_user()
    return redirect('/login')
  
  # 記事登録画面
  @app.route('/register')
  @login_required
  def register():
    return render_template('register.html')
  
  # 記事の表示
  @app.route('/all')
  @login_required
  def all():
    return render_template('all.html', all='all')

  return app