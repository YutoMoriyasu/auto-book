import os

from flask import Flask, render_template, request, redirect
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash

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
  def index():
    # TODO ユーザーに対して、登録しているグループの情報を取得する処理を記述する
    test = 'テンプレートエンジンのテスト'
    return render_template('index.html', test=test)

  # 個別のグループページ
  @app.route('/groups/<group_id>') # /groups/<group_id>にアクセスしたとき
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
    return render_template('login.html')


  return app