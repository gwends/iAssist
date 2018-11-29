from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError, AnyOf, Length, Email, EqualTo

from app.models import User


class JobPostForm(FlaskForm):
    job_type = SelectField('Job Type', choices=[
        ('FT', 'Full Time'), ('PT', 'Part Time')])
    description = StringField('Job Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    salary = IntegerField('Salary Offer', validators=[DataRequired()])
    maxWorker = IntegerField('Max Worker', validators=[DataRequired()])


class EmployeeJobPostForm(FlaskForm):
    job_type = StringField(
        'Job Title*',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
        ]
    )
    contact = StringField(
        'Location',
        validators=[
            DataRequired(),
            Length(min=3, max=20)
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


class JobPostForm(FlaskForm):
    title = StringField(
        'Job Title',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
        ]
    )
    location = StringField(
        'Location',
        validators=[
            DataRequired(),
            Length(min=3, max=20)
        ]
    )
    salary = StringField(
        'Salary',
        validators=[
            DataRequired()
        ]
    )
    description = TextAreaField(
        'Job Description',
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )
    contact_details = StringField(
        'Contact Number',
        validators=[

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
    category = SelectField(
        choices=[
            ('Post', 'Employee'),
            ('Offer', 'Employer')
        ]
    )
    submit = SubmitField(
        'Search'
    )
