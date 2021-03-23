from flask import Blueprint, render_template
from files.models import Category

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html", Category=Category), 404
    
@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html", Category=Category), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/404.html", Category=Category), 500
    
@errors.app_errorhandler(401)
def error_401(error):
    return render_template("errors/403.html", Category=Category), 401