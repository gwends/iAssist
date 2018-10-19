from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, ValidationError, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, InputRequired, EqualTo, DataRequired, Email



class Register(FlaskForm):
	username = StringField('Username' ,render_kw = {'placeholder': 'Username'},validators = [InputRequired(), Length(min = 6, max = 30)])
	password = PasswordField('Password',render_kw = {'placeholder': 'Password'}, validators = [InputRequired(), Length(min = 8, max = 30)])
	confirm = PasswordField('Confirm Password',render_kw = {'placeholder': 'Confirm Password'}, validators = [DataRequired(), EqualTo('password', message = 'Password Mismatch')])
	firstname = StringField('First Name',render_kw = {'placeholder': 'Firstname'}, validators = [InputRequired(), Length(min=3, max= 20)])
	lastname = StringField('Last Name', render_kw = {'placeholder': 'Lastname'}, validators= [InputRequired(), Length(min=2, max = 20)])
	contact = StringField('Contact No.',render_kw = {'placeholder': 'Contact'}, validators = [InputRequired(), Length(11)])
	gender = RadioField('Gender', render_kw = {'placeholder': 'Gender'}, validators = [InputRequired()], choices = [('Male', 'Male'), ('Female', 'Female')], default = 'Male')
	birthdate= DateField('Birth Date', format='%d-%m-%Y',render_kw = {'placeholder': 'Birthdate'}, validators=[DataRequired(),InputRequired()])
	email = StringField("Email Address", render_kw = {'placeholder': 'Email Address'},validators = [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])