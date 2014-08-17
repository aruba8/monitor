from bson.objectid import ObjectId

__author__ = 'erik'
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField, HiddenField
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


class HostAddForm(Form):
    host = StringField('Host', id='host', validators=[URL(require_tld=False, message=u'Invalid URL.'), DataRequired()])
    xpath = StringField('Xpath', id='xpath', validators=[DataRequired()])
    submit = SubmitField(label='Submit', id='submit', default='add')


class HostEditForm(Form):
    edit = HiddenField(id='edit-input')
    host_to_edit = StringField(label='Host')
    edit_xpath_field = StringField(label='Xpath')
    edit_submit = SubmitField('Save')

