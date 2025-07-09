# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, TextAreaField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    file = FileField('PDF File', validators=[DataRequired()])
    submit = SubmitField('Upload')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    level = SelectField('Level', choices=[
        ('Class 10', 'Class 10'),
        ('PUC', 'PUC'),
        ('Degree', 'Degree'),
        ('Competitive', 'Competitive')
    ], validators=[DataRequired()])
    type = SelectField('Type', choices=[
        ('Notes', 'Notes'),
        ('Question Paper', 'Question Paper'),
        ('Model Paper', 'Model Paper')
    ], validators=[DataRequired()])
    pdf_file = FileField('Upload PDF', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDFs only!')
    ])
    submit = SubmitField('Upload')


class EditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Update')

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")

