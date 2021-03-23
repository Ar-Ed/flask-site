from files.models import Category

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/main')
@main.route('/home')
def home():
    return render_template("home.html", Category=Category)