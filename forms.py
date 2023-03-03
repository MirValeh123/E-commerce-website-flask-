from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,TextAreaField,EmailField
from wtforms.validators import DataRequired, Email, EqualTo,Length


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'password', validators=[DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),Length(min=5,max=20)])
    email = EmailField("Email", validators=[DataRequired(),Email(),Length(min=10,max=30)] )
    subject=StringField('Subject',validators=[DataRequired()])
    messages=TextAreaField('Message',validators=[DataRequired()])


class CommentForm(FlaskForm):
    comment=TextAreaField('Comment',validators=[DataRequired()])

