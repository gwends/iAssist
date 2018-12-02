from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError, AnyOf, Length, Email, EqualTo

from app.models import User


class EmployerPostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    salary = IntegerField('Salary Offer', validators=[DataRequired()])
    maxWorker = IntegerField('Available Count', validators=[DataRequired()])
    job_type = SelectField('Job Category',
                           choices=[
                               ('PT', 'Part Time'),
                               ('FT', 'Full Time')
                           ]
                           )
    submit = SubmitField('Post')


class SeekerPostForm(FlaskForm):
    stitle = StringField('Job Title', validators=[DataRequired()])
    sdescription = TextAreaField(
        'Job Description', validators=[DataRequired()])
    slocation = StringField('Location', validators=[DataRequired()])
    ssalary = IntegerField('Target Salary', validators=[DataRequired()])
    sjob_type = SelectField('Job Category',
                            choices=[
                                ('PT', 'Part Time'),
                                ('FT', 'Full Time')
                            ]
                            )
    ssubmit = SubmitField('Post')


class SearchForm(FlaskForm):
    search = StringField(
        '',
        validators=[
            DataRequired()
        ]
    )
    category = SelectField(
        choices=[
            ('Employer', 'Seeker'),
            ('Seeker', 'Employer')
        ]
    )
    submit = SubmitField(
        'Search'
    )
