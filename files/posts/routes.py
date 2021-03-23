import secrets
import os
from files import db
from flask import render_template, redirect, url_for, flash, request, Blueprint
from files.models import Article, User, Comment, Category
from files.posts.forms import AdminForm, CommentForm, CategoryForm
from flask_login import current_user, login_required
from datetime import datetime, timezone

posts = Blueprint('posts', __name__)

@posts.route('/articles/<article_name>', methods=['GET', 'POST']) # dynamic route
def article(article_name):
    comment_section = request.args.get("comment_section", 1, type=int)
    article = Article.query.filter_by(title = article_name).first()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(user_id=current_user.id, article_id=Article.query.filter_by(title = article_name).first().id, user_comment= form.comment.data, date=datetime.utcnow())
        db.session.add(comment)
        db.session.commit()
        flash(f"Comment is Posted!", category='succesful')
        return redirect(url_for("posts.article", article_name=article_name))
    else:
        for error in form.errors.values():
            flash(f"{error[0]}", category='danger')

    return render_template("article.html", article_name=article_name, article=article, 
    Comments=Comment.query.filter_by(article_id=article.id).order_by(Comment.id.desc()).paginate(per_page=5, page=comment_section), 
    current_user=current_user, form=form, Category=Category, User=User)#timezone=handler.getDetails(ip_address=request.remote_addr).timezone # timezone won't work due to localhost

@posts.route('/articles')
def articles():
    page = request.args.get("page", 1, type=int)
    return render_template("articles.html", Articles=Article.query.order_by(Article.id.desc()).paginate(per_page=5, page=page), now = datetime.utcnow(), timezone=timezone, User=User, Category=Category, page=page)

@posts.route('/admin_page', methods=['GET', 'POST'])
@login_required
def admin_control():
    if current_user.user_name != "Admin":
        return redirect(url_for("main.home"))
    form = AdminForm()
    form_category = CategoryForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, article_content=form.article_content.data, abstract=form.abstract.data, user_id=current_user.id, category_id=Category.query.filter_by(category_name=form.category.data).first().id)
        db.session.add(article)
        db.session.commit()
        flash("Article is published", category='success')
        return redirect(url_for("posts.article", article_name=form.title.data))
    
    if form_category.validate_on_submit():
        category = Category(category_name=form_category.category.data)
        db.session.add(category)
        db.session.commit()
        flash("Category is added", category='success')
        return redirect(url_for("posts.category", category=form_category.category.data))
    
    if form.errors:
        for error in form.errors.values():
            flash(f"{error[0]}", category='danger')

    if form_category.errors:
        for error in form_category.errors.values():
            flash(f"{error[0]}", category='danger')

    return render_template("admin.html", form = form, form_category=form_category, Category=Category)

@posts.route('/<category>')
def category(category):
    category_ = Category.query.filter_by(category_name = category).first()
    page = request.args.get("page", 1, type=int)
    return render_template("category.html", Article=Article.query.filter_by(category_id=category_.id).order_by(Article.id.desc()).paginate(per_page=5, page=page),
     now = datetime.utcnow(), timezone=timezone, category_=category_, Category=Category)