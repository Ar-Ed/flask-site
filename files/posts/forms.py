from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from files.models import Article, Category

class AdminForm(FlaskForm):
    title = StringField(label = "Title", validators=[Length(min=0,max=100, message="Length of the article title has to be between 0 and 50"), DataRequired(message="Title can't be empty")])
    article_content = TextAreaField(label = "Article Content", validators=[Length(min=0,max=10000, message="Length of the article body has to be between 0 and 10000"), DataRequired(message="Article content can't be empty")])
    abstract = TextAreaField(label = "Absract", validators=[Length(min=0,max=150, message="Length of the abstract has to be between 0 and 150"), DataRequired(message="Abstract can't be empty")])
    category = StringField(label = "Category", validators=[Length(min=2,max=50, message="Length of the category has to be between 2 and 50"), DataRequired(message="Category can't be empty")])
    
    submit = SubmitField(label="Post")

    def validate_article_name(self,title):
        article = Article.query.filter_by(title=title.data).first()
        if article:
            raise ValidationError("An article with this name is already published!")

class CategoryForm(FlaskForm):
    category = StringField(label = "Category Name", validators=[Length(min=2,max=50, message="Length of the Category name has to be between 0 and 50"), DataRequired(message="Category name can't be empty")])
    submit = SubmitField(label="Create Category")

    def validate_category_name(self,category):
        category_ = Category.query.filter_by(category_name=category.data).first()
        if category_:
            raise ValidationError("A category is already created with this name!")

class CommentForm(FlaskForm):
    comment = TextAreaField(validators=[Length(max=150, message='Maximum comment length is 150'), DataRequired(message="You can't comment empty text")])
    submit = submit = SubmitField(label="Comment")