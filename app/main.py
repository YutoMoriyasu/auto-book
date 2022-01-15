from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.auth import *
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
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
  individual_groups = Group.query.filter_by(user_id = current_user.id)
  data = {}
  for individual_group in individual_groups:
    data[individual_group.id] = []
    relations = GroupPost.query.filter_by(group_id = individual_group.id)
    for relation in relations:
      post = Post.query.filter_by(id = relation.post_id).first()
      data[individual_group.id].append(post)
  return render_template('index.html', groups=individual_groups, data = data)

# 個別のグループページ
@main.route('/groups/<group_id>') # /groups/<group_id>にアクセスしたとき
@login_required
def group(group_id):
  group = Group.query.filter_by(id = group_id).first()
  relations = GroupPost.query.filter_by(group_id = group_id)
  posts_in_group = []
  for relation in relations:
    post = Post.query.filter_by(id = relation.post_id).first()
    posts_in_group.append(post)
  return render_template('group.html', posts = posts_in_group, group_name = group.name) # group.htmlに変数group_idを渡す

@main.route('/groups/create')
@login_required
def groups_create():
  return render_template('create_group.html')

@main.route('/groups/create', methods=['POST'])
def groups_create_post():
  current_url = request.form.get('current_path')
  group_name = request.form.get('group_name')

  groups = Group.query.filter_by(name = group_name)
  group_name_is_used = False
  for group in groups:
    if (group.name == group_name) & (group.user_id == current_user.id):
      group_name_is_used = True
      break

  if group_name_is_used:
    flash('同じグループ名が使われています。異なるグループ名を入力してください。')
    return redirect(current_url)
  else:
    user_id = current_user.id
    new_group = Group(user_id = user_id, name = group_name, created_at = datetime.datetime.now())

    db.session.add(new_group)
    db.session.commit()
    return redirect(current_url)

# 記事登録画面
@main.route('/register', methods=['POST'])
def register_post():
  current_url = request.form.get('current_path')
  group_id = request.form.get('group_id')
  post_url = request.form.get('article_url')
  login_user_id = current_user.id
  res = requests.get(post_url)
  soup = BeautifulSoup(res.text, 'html.parser')
  post_title = soup.find('title').text

  posts = Post.query.filter_by(title = post_title)
  post_is_registered = False
  for post in posts:
    if (post.title == post_title) & (login_user_id == post.user_id):
      post_is_registered = True
      break
  if post_is_registered:
    flash('記事がすでに登録されています。')
    return redirect(current_url)
  else:
    new_post = Post(user_id = login_user_id, url = post_url, title = post_title, created_at = datetime.datetime.now())
    db.session.add(new_post)
    db.session.commit()
    if group_id:
      post = Post.query.filter_by(title = post_title).first()
      new_relation = GroupPost(group_id = group_id, post_id = post.id)
      db.session.add(new_relation)
      db.session.commit()
    return redirect(current_url)

# 記事の表示
@main.route('/posts')
@login_required
def posts():
  individual_posts = Post.query.filter_by(user_id = current_user.id)
  individual_groups = Group.query.filter_by(user_id = current_user.id)
  return render_template('posts.html', posts = individual_posts, groups = individual_groups)

@main.route('/create_relation', methods=['POST'])
def create_relation():
  post_id = request.form.get('post_id')
  group_id = request.form.get('group_id')

  new_relation = GroupPost(group_id = group_id, post_id = post_id)

  db.session.add(new_relation)
  db.session.commit()
  return redirect(url_for('main.posts'))
