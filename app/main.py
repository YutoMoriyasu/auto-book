from app.auth import *
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

# トップページ
@main.route('/')
@login_required
def index():
  # TODO ユーザーに対して、登録しているグループの情報を取得する処理を記述する
  test = 'テンプレートエンジンのテスト'
  return render_template('index.html', test=current_user.name)

# 個別のグループページ
@main.route('/groups/<group_id>') # /groups/<group_id>にアクセスしたとき
@login_required
def group(group_id):
  # TODO 個別のグループの情報を取得する処理を記述する
  return render_template('group.html', group_id=group_id) # group.htmlに変数group_idを渡す

# 記事登録画面
@main.route('/register')
@login_required
def register():
  return render_template('register.html')

# 記事の表示
@main.route('/all')
@login_required
def all():
  return render_template('all.html', all='all')
