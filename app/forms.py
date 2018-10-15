from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Regexp, ValidationError, AnyOf, Length


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
