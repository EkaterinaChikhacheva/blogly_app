"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):

    __tablename__='users'

    '''User table'''
    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    first_name = db.Column(db.String(50),
                    nullable = False)

    last_name = db.Column(db.String(50),
                     nullable = False)

    image_url = db.Column(db.String(), nullable = False, default = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5UhZeoomfYvjzT12orXk6q-2LPXhAyTx2lZEAOEt8QDDXM2jIH2S1ubwiHoZOEEGAP_g&usqp=CAU')

    post = db.relationship('Post', backref = 'users')



    def __repr__(self):
        '''show info about pet'''
        u = self
        return f'''<User id = {u.id} 
                    first_name ={u.first_name}  
                    last_name = {u.last_name} 
                    image_url = {u.image_url}>'''

    def update(self, fn, ln, img):
        self.first_name = fn
        self.last_name = ln
        self.image_url = img


class Post(db.Model):

    __tablename__ ='posts'

    '''Posts table'''

    id = db.Column(
                    db.Integer, 
                    primary_key=True, 
                    autoincrement = True)

    title = db.Column(
                    db.String, 
                    nullable=False)

    content = db.Column(
                    db.Text, 
                    nullable=False)

    created_at = db.Column(
                    db.DateTime,
                    nullable=False,
                    default=datetime.datetime.now)

    user_id = db.Column(
                    db.Integer, 
                    db.ForeignKey('users.id'), 
                    nullable=False)



    def __repr__(self):
        '''show info about pet'''
        p = self
        return f'''<Post id = {p.id} 
                    title ={p.title}  
                    content = {p.content} 
                    created_at = {p.created_at}, 
                    user_id = {p.user_id}>'''

    def update(self, tl, cnt, time, user):
        self.title = tl
        self.content = cnt
        self.created_at = time
        self.user_id = user


def connect_db(app):
    db.app = app
    db.init_app(app)
