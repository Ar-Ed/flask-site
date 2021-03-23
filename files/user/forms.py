from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from files.models import User, Article, Category
from flask_login import current_user


class AccountForm(FlaskForm):
    username = StringField(label = "User Name", validators=[Length(min=2,max=20, message="Length of the user name has to be between 2 and 20"), DataRequired(message="User Name can't be empty")])
    username_new = StringField(label = "New User Name", validators=[Length(min=2,max=20, message="Length of the new user name has to be between 2 and 20")])
    password = PasswordField(label = "Old Password", validators=[DataRequired(message="Password can't be empty"), Length(min=6,max=30, message="Length of the password has to be between 6 and 30")])
    password_new = PasswordField(label = "New Password", validators=[Length(min=6,max=30, message="Length of the new password has to be between 6 and 30")])
    image = FileField('Update profile picture', validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField(label="Update")

    def validate_username(self,username_new):
        if username_new.data != current_user.user_name:
            user = User.query.filter_by(user_name=username_new.data).first()
            if user:
                raise ValidationError("This username is already taken")
    def validate_password(self,password):
        if not bcrypt.check_password_hash(current_user.password,password.data):
            raise ValidationError("Password is incorrect")

class LoginForm(FlaskForm):
    username = StringField(label = "User Name", validators=[Length(min=2,max=20, message="Length of the user name has to be between 2 and 20"), DataRequired(message="User Name can't be empty")])
    password = PasswordField(label = "Password", validators=[DataRequired(message="Password can't be empty"), Length(min=6,max=30, message="Length of the password has to be between 6 and 30")])
    submit = SubmitField(label="Login")

class RegisterForm(FlaskForm):
    username = StringField(label = "User Name", validators=[Length(min=2,max=20, message="Length of the user name has to be between 2 and 20"), DataRequired(message="User Name can't be empty")])
    password = PasswordField(label = "Password", validators=[DataRequired(message="Password can't be empty"), Length(min=6,max=30, message="Length of the password has to be between 6 and 30")])
    password_check = PasswordField(label = "Repeat Password", validators=[EqualTo('password', message="Passwords does not match"),DataRequired(message="Password can't be empty")])
    submit = SubmitField(label="Register")

    def validate_username(self,username):
        user = User.query.filter_by(user_name=username.data).first()
        if user:
            raise ValidationError("This user name is already taken!")