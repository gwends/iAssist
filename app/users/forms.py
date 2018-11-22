from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError, AnyOf, Length, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    remember_me = BooleanField(
        'Remember me'
    )
    submit = SubmitField(
        'Sign In'
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )
    firstname = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Regexp('^[A-Za-z ]{2,30}$', message="Enter a valid First name.")
        ]
    )
    lastname = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Regexp('^[A-Za-z ]{2,30}$', message="Enter a valid Last name.")
        ]
    )
    gender = RadioField(
        'Gender',
        choices=[
            ('M', 'Male'),
            ('F', 'Female')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    contact_no = StringField(
        'Contact No.',
        validators=[
            DataRequired(),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    check_password = PasswordField(
        'Repeat Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField(
        'Register'
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'Username already Exists! Please use a different one')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError(
                'Email already in use! Please use a different one')


class EditProfile(FlaskForm):
    firstname = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Regexp('^[A-Za-z ]{2,30}$', message="Enter a valid First name.")
        ]
    )
    lastname = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Regexp('^[A-Za-z ]{2,30}$', message="Enter a valid Last name.")
        ]
    )
    gender = RadioField(
        'Gender',
        choices=[
            ('M', 'Male'),
            ('F', 'Female')
        ]
    )
    contact_no = StringField(
        'Contact No.',
        validators=[
        ]
    )
    edu_background = StringField(
        'Educational Background',
    )
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField(
        'Edit'
    )
