from files import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False,unique=True)
    article_content = db.Column(db.Text)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    abstract = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="article", lazy = True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False, unique=True)
    article_cat = db.relationship("Article", backref="category", lazy = True)

class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    ip_address = db.Column(db.String(30))
    comments = db.relationship("Comment", backref="user", lazy = True)
    articles = db.relationship("Article", backref="user", lazy = True)
    image = db.Column(db.String(30), default="default.png")  

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_comment = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    #parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    #replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]),lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)