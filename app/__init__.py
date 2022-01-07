import os

from flask import Flask, render_template, request, redirect
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

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
      passward = request.form.get('passward')
      # Userのインスタンスを作成
      user = User(username=username, password=generate_password_hash(password, method='sha256'))
      db.session.add(user)
      db.session.commit()
      return redirect('/login')
    else:
      return render_template('signup.html')

  # ログイン画面
  @app.route('/login')
  def login():
    if request.method == "POST":
      username = request.form.get('username')
      password = request.form.get('password')
      user = User.query.filter_by(username=username).first()
      if check_password_hash(user.password, password):
        login_user(user)
        return redirect('/')
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