__author__ = 'erik'
from flask.ext.wtf import Form
from wtforms.fields import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import Required, Length, DataRequired


class LoginForm(Form):
    login = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
