"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'never_tell_123!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def empty():
    return redirect('/users')

@app.route('/users')
def list_users():
    '''Show a page with all the users in db'''
    users = User.query.all()
    return render_template('users_page.html', users = users)

@app.route('/users/new')
def add_user_pg():
    '''Show an add form for users'''
    return render_template('add_user_pg.html')

@app.route('/users/new', methods = ['POST'])
def handle_submit():
    '''Proccesing user's form submit, adding to the db'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    '''Show information about the given user.'''
    user = User.query.get_or_404(user_id)
    return render_template('user_details_page.html', user = user)

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    '''Show the edit page for a user.'''
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_pg.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def handle_edit(user_id):
    '''Update the db accordingly'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)
    user.update(first_name,last_name,image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def detele_user(user_id):
    '''Remove the user from db'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """ Show the user an add s post form"""
    user = User.query.get_or_404(user_id)
    return render_template('add_post.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def handle_add_post_form(user_id):
    '''Handle add form; add post to the db and redirect to the user detail page.'''

    title = request.form['title']
    content = request.form['content']
    created_at = datetime.now()
    user = User.query.get(user_id)
###############################
    new_post = Post(title = title, content = content, created_at = created_at, user_id = user_id )
    # new_post.Post.update(title,content,created_at,user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

