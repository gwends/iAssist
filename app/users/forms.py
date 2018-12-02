from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, SubmitField, SelectField, DateField, TextAreaField, RadioField, PasswordField, BooleanField
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
            DataRequired(),
            Regexp(
                '^[a-zA-Z0-9]{1,30}$', message="Invalid Username, No Special characters Allowed."),
            Length(min=5, max=20, message="Username too short or too long.")
        ]
    )
    firstname = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Regexp('^[A-Za-z ]{2,30}$', message="Invalid First Name.")
        ]
    )
    lastname = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Regexp('^[A-Za-z ]{2,30}$', message="Invalid Last Name.")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=[
            ('', 'Gender'),
            ('M', 'Male'),
            ('F', 'Female')
        ], validators=[AnyOf(['M', 'F'], message='Please Choose your Gender')]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Invalid Email.")
        ]
    )
    contact_no = StringField(
        'Contact No.',
        validators=[
            DataRequired(),
            Regexp('^(09|\+639)\d{9}$',
                   message="Invalid Mobile Number.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=5, message="Password too short.")
        ]
    )
    check_password = PasswordField(
        'Repeat Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    location = StringField(
        'Current Address',
        validators=[
            Regexp('^[A-Za-z0-9 ]{2,30}$', message='Invalid Location')
        ]
    )
    birthDate = StringField('Birth Date', validators=[], render_kw={
        'data-format': "Y-m-d",
    })

    terms = BooleanField('Terms and Agreements', validators=[DataRequired(
        message='I need you to agree for our terms and agreements before we can register you.')])

    agree = BooleanField('Agree?', validators=[DataRequired(
        message='You need to agree that this is for local use only.')])

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
            Regexp('^[A-Za-z ]{2,30}$', message="Invalid First Name.")
        ]
    )
    lastname = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Regexp('^[A-Za-z ]{2,30}$', message="Invalid Last Name.")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=[
            ('', 'Gender'),
            ('M', 'Male'),
            ('F', 'Female')
        ], validators=[AnyOf(['M', 'F'], message='Please Choose your Gender')]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Invalid Email.")
        ]
    )
    contact_no = StringField(
        'Contact No.',
        validators=[
            DataRequired(),
            Regexp('^(09|\+639)\d{9}$',
                   message="Invalid Mobile Number.")
        ]
    )
    location = StringField(
        'Current Address',
        validators=[
            Regexp('^[A-Za-z0-9 ]{2,30}$', message='Invalid Location')
        ]
    )
    submit = SubmitField(
        'Edit'
    )


class EditIMG(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[DataRequired(message='No File Found!'),
                                                              FileAllowed(['jpg', 'png'], message='Only jpg and png files can be uploaded.')])
    submit = SubmitField(
        'Upload'
    )
