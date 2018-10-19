from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError, AnyOf, Length, Email, EqualTo

from app.models import User


class EmployeeJobPostForm(FlaskForm):
    title = StringField(
        'Job Title*',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
        ]
    )
    address = StringField(
        'Location',
        validators=[
            DataRequired(),
            Length(min=3, max=20)
        ]
    )
    salary_price = StringField(
        'Salary',
        validators=[

        ]
    )
    salary_category = SelectField(
        choices=[
            ('None', 'Salary Type'),
            ('D', 'Per Day'),
            ('H', 'Per Hour')
        ],
        validators=[
            AnyOf(('H', 'D'))
        ]
    )
    contact_details = StringField(
        'Contact Number*',
        validators=[

        ]
    )
    description = TextAreaField(
        'Job Description',
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )
    submit = SubmitField('Post Job')


class HirerJobPostForm(FlaskForm):
    title = StringField(
        'Job Title',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
        ]
    )
    address = StringField(
        'Location',
        validators=[
            DataRequired(),
            Length(min=3, max=20)
        ]
    )
    salary_price = StringField(
        'Salary',
        validators=[

        ]
    )
    salary_category = SelectField(
        choices=[
            ('None', '<--- Optional --->'),
            ('D', 'Per Day'),
            ('H', 'Per Hour')
        ]
    )

    description = TextAreaField(
        'Job Description',
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )
    submit = SubmitField('Post Job')


class SearchForm(FlaskForm):
    search = StringField(
        '',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        'Search'
    )


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
            DataRequired()
        ]
    )
    lastname = StringField(
        'Last Name',
        validators=[
            DataRequired()
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
