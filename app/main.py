from turtle import pos
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.auth import *
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from bs4 import BeautifulSoup
import requests
import datetime
import uuid
from . import db
from .models import *

main = Blueprint('main', __name__)

# トップページの表示
@main.route('/', methods=['GET'])
@login_required
def index():
  individual_groups = Group.query.filter_by(user_id = current_user.id)
  data = {}
  grouped_post_comment_data = {}
  for individual_group in individual_groups:
    data[individual_group.id] = []
    relations = GroupPost.query.filter_by(group_id = individual_group.id)
    for relation in relations:
      post = Post.query.filter_by(id = relation.post_id).first()
      grouped_post_comments = Comment.query.filter_by(post_id = post.id)
      grouped_post_comment_data[post.id] = []
      if post.is_archived == True:
        continue
      for comment in grouped_post_comments:
        grouped_post_comment_data[post.id].append(comment)
      data[individual_group.id].append(post)

  ungrouped_posts = []
  ungrouped_post_comment_data = {}
  posts = Post.query.filter_by(user_id = current_user.id)
  for post in posts:
    relation = GroupPost.query.filter_by(post_id = post.id).first()
    ungrouped_post_comments = Comment.query.filter_by(post_id = post.id)
    ungrouped_post_comment_data[post.id] = []
    if relation:
      continue
    elif post.is_archived == True:
      continue
    else:
      for comment in ungrouped_post_comments:
        ungrouped_post_comment_data[post.id].append(comment)
      ungrouped_posts.append(post)

  return render_template('index.html', groups=individual_groups, data = data, ungrouped_posts = ungrouped_posts, grouped_post_comment_data = grouped_post_comment_data, ungrouped_post_comment_data = ungrouped_post_comment_data)

# グループ一覧の表示
@main.route('/groups/all', methods=['GET'])
@login_required
def list_groups():
  groups = Group.query.filter_by(user_id = current_user.id)
  return render_template('group_list.html', groups = groups)

# 個別のグループページの表示
@main.route('/groups/<group_id>', methods=['GET'])
@login_required
def group(group_id):
  groups = Group.query.filter_by(user_id = current_user.id)
  group = Group.query.filter_by(id = group_id).first()
  relations = GroupPost.query.filter_by(group_id = group_id)
  posts_in_group = []
  for relation in relations:
    post = Post.query.filter_by(id = relation.post_id).first()
    if post.is_archived == True:
      continue
    posts_in_group.append(post)
  
  comment_data = {}
  for post in posts_in_group:
    comment_data[post.id] = []
    comments = Comment.query.filter_by(post_id = post.id)
    for comment in comments:
      comment_data[post.id].append(comment)
  return render_template('group.html', posts = posts_in_group, group_name = group.name, groups = groups, comments = comment_data)

# グループ作成
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
    new_group = Group(id = str(uuid.uuid4()), user_id = user_id, name = group_name, created_at = datetime.datetime.now())

    db.session.add(new_group)
    db.session.commit()
    return redirect(current_url)

# 記事登録
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
@main.route('/posts', methods=['GET'])
@login_required
def posts():
  individual_posts = Post.query.filter_by(user_id = current_user.id, is_archived = False)
  individual_groups = Group.query.filter_by(user_id = current_user.id)
  comment_data = {}
  for post in individual_posts:
    comment_data[post.id] = []
    comments = Comment.query.filter_by(post_id = post.id)
    for comment in comments:
      comment_data[post.id].append(comment)
  return render_template('posts.html', posts = individual_posts, groups = individual_groups, comments = comment_data)

# 記事とグループの関連付け
@main.route('/create_relation', methods=['POST'])
def create_relation():
  current_url = request.form.get('current_path')
  post_id = request.form.get('post_id')
  group_id = request.form.get('group_id')
  group_name = Group.query.filter_by(id = group_id).first().name

  old_relation = GroupPost.query.filter_by(group_id = group_id, post_id = post_id).first()
  if old_relation:
    flash('この記事はすでに「' + group_name + '」に追加されています。')
    return redirect(current_url)

  else:
    new_relation = GroupPost(group_id = group_id, post_id = post_id)

    db.session.add(new_relation)
    db.session.commit()
    return redirect(current_url)

# 記事のアーカイブ
@main.route('/archive_post', methods=['POST'])
def archive_post():
  current_url = request.form.get('current_path')
  post_id = request.form.get('post_id')

  post = Post.query.filter_by(id = post_id).first()
  post.is_archived = True

  flash(post.title + 'がアーカイブされました。')

  db.session.add(post)
  db.session.commit()

  return redirect(current_url)

# アーカイブ記事の復元
@main.route('/archives/restore', methods=['POST'])
def restore_post():
  current_url = request.form.get('current_path')
  post_id = request.form.get('post_id')

  post = Post.query.filter_by(id = post_id).first()
  post.is_archived = False

  flash(post.title + 'が復元されました。')

  db.session.add(post)
  db.session.commit()

  return redirect(current_url)

# アーカイブの表示
@main.route('/archives', methods=['GET'])
@login_required
def archives():
  login_user_id = current_user.id
  posts = Post.query.filter_by(user_id = login_user_id, is_archived = True)

  return render_template('archives.html', posts = posts)

@main.route('/leave-comment', methods=['POST'])
def leave_comment():
  current_url = request.form.get('current_url')
  post_id = request.form.get('post_id')
  comment_text = request.form.get('text')
  new_comment = Comment(post_id = post_id, text = comment_text, created_at = datetime.datetime.now())
  db.session.add(new_comment)
  db.session.commit()

  return redirect(current_url)