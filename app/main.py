from app.auth import *
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from bs4 import BeautifulSoup
import requests
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

@main.route('/register', methods=['POST'])
def register_post():
  post_url = request.form.get('article_url')
  login_user_id = current_user.id

  res = requests.get(post_url)
  soup = BeautifulSoup(res.text, 'html.parser')
  post_title = soup.find('title').text

  new_post = Post(user_id = login_user_id, url = post_url, title = post_title)

  db.session.add(new_post)
  db.session.commit()
  return redirect(url_for('main.all'))

# 記事の表示
@main.route('/all')
@login_required
def all():
  individual_posts = Post.query.filter_by(user_id = current_user.id)
  return render_template('all.html', posts = individual_posts)
