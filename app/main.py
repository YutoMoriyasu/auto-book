from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.auth import *
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from bs4 import BeautifulSoup
import requests
import datetime
from . import db
from .models import *

main = Blueprint('main', __name__)

# トップページ
@main.route('/')
@login_required
def index():
  # TODO ユーザーに対して、登録しているグループの情報を取得する処理を記述する
  individual_groups = Group.query.filter_by(user_id = current_user.id)
  return render_template('index.html', groups=individual_groups)

# 個別のグループページ
@main.route('/groups/<group_id>') # /groups/<group_id>にアクセスしたとき
@login_required
def group(group_id):
  # TODO 個別のグループの情報を取得する処理を記述する
  return render_template('group.html', group_id=group_id) # group.htmlに変数group_idを渡す


@main.route('/groups/create')
@login_required
def groups_create():
  return render_template('create_group.html')

@main.route('/groups/create', methods=['POST'])
def groups_create_post():
  group_name = request.form.get('group_name')
  user_id = current_user.id
  new_group = Group(user_id = user_id, name = group_name, created_at = datetime.datetime.now())

  db.session.add(new_group)
  db.session.commit()
  return redirect(url_for('main.index'))

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

  new_post = Post(user_id = login_user_id, url = post_url, title = post_title, created_at = datetime.datetime.now())

  db.session.add(new_post)
  db.session.commit()
  return redirect(url_for('main.all'))

# 記事の表示
@main.route('/all')
@login_required
def all():
  individual_posts = Post.query.filter_by(user_id = current_user.id)
  return render_template('all.html', posts = individual_posts)
