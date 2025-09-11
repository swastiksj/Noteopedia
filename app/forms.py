# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileRequired, FileAllowed


# Admin Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# Upload Form
class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    level = SelectField(
        'Level',
        choices=[
            ('Class 10', 'Class 10'),
            ('PUC', 'PUC'),
            ('Degree', 'Degree'),
            ('Competitive', 'Competitive')
        ],
        validators=[DataRequired()]
    )
    type = SelectField(
        'Type',
        choices=[
            ('Notes', 'Notes'),
            ('Question Paper', 'Question Paper'),
            ('Study Material', 'Study Material')
        ],
        validators=[DataRequired()]
    )
    pdf_file = FileField(
        'Upload PDF',
        validators=[
            FileRequired(),
            FileAllowed(['pdf'], 'PDFs only!')
        ]
    )
    submit = SubmitField('Upload')


# Edit Form
class EditForm(FlaskForm):
    title = StringField('Title')
    subject = StringField('Subject')
    file = FileField('Upload PDF')
    submit = SubmitField('Update')


# Contact Form
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")


# Student Question Form
class QuestionForm(FlaskForm):
    question = StringField('Your Question', validators=[DataRequired()])
    submit = SubmitField('Ask')
