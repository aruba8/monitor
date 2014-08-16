from bson.objectid import ObjectId

__author__ = 'erik'
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL


class LoginForm(Form):
    login = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignUpForm(Form):
    login = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm')
    secret = StringField('Secret', validators=[DataRequired()])


class AddURLForm(Form):
    url = StringField('URL', validators=[URL(require_tld=False, message=u'Invalid URL.')])
    host_id = SelectField(coerce=ObjectId)
