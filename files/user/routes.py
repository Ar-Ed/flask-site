import secrets
import os
from files import db, bcrypt, handler
from flask import render_template, redirect, url_for, flash, request, Blueprint
from files.models import Article, User, Comment, Category
from files.user.forms import RegisterForm, LoginForm, AccountForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timezone
from files.user.utils import save_image

users = Blueprint('users', __name__)

@users.route('/users/<user_name>', methods=['GET', 'POST'])
def account_page(user_name):
    form = AccountForm()
    if current_user.is_authenticated and current_user.user_name == user_name:
        if request.method == "GET":
            form.username.data = current_user.user_name
            form.username_new.data = current_user.user_name
        if form.validate_on_submit():
            if form.image.data:
                if current_user.image:
                    os.remove(os.path.join(os.path.dirname(__file__), url_for("static", filename="img/" + current_user.image)[1:]))
                image_file = save_image(form.image.data)
                current_user.image = image_file
                flash("Profile picture has been updated", category='success')
            if form.password_new.data:
                current_user.password= bcrypt.generate_password_hash(form.password_new.data).decode('utf-8')
                flash("Password has been updated", category='success')
            if form.username_new.data:
                current_user.user_name= form.username_new.data
                flash("User name has been updated", category='success')
            db.session.commit()
            flash("Your info has been updated", category="succesful")
            return redirect(url_for('users.account_page', user_name=current_user.user_name))
        if form.errors:
            for error in form.errors.values():
                flash(f"{error[0]}", category='danger')
    image_file = url_for("static", filename="img/" + User.query.filter_by(user_name=user_name).first().image)
    return render_template("account.html", User=User, user_name=user_name, image_file=image_file, Category=Category, form=form, current_user=current_user, Comment=Comment, datetime=datetime)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():  
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        hashed_ip = bcrypt.generate_password_hash(request.remote_addr).decode('utf-8')
        user = User(user_name=form.username.data,password=hashed_password,ip_address=hashed_ip)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        flash("Created Account", category='success')
        return redirect(next_page) if next_page else redirect(url_for("main.home"))  
    if form.errors:
        for error in form.errors.values():
            flash(f"{error[0]}", category='danger')

    return render_template("register.html", form = form, Category=Category)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("Logged In", category='success')
            next_page = request.args.get('next') ## in case i decide to do something exclusive to users
            return redirect(next_page) if next_page else redirect(url_for("main.home"))  
        else:
            flash("Password or Username is not correct", category='danger')
    if form.errors:
        for error in form.errors.values():
            flash(f"{error[0]}", category='danger')
    return render_template("login.html", form = form, Category=Category)

@users.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged Out', category="success")
    return redirect(url_for("main.home"))