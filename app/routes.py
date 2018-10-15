from app import app
from flask import render_template

from app.forms import EmployeeJobPostForm, HirerJobPostForm


@app.route('/')
def index():
    return render_template('land_page.html', title="Home")


@app.route('/job_apply')
def job_apply():
    employeeForm = EmployeeJobPostForm()
    hirerForm = HirerJobPostForm()
    return render_template('job_apply.html', title="Job Apply", eform=employeeForm, hform=hirerForm)
