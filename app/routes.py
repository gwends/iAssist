from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.forms import EmployeeJobPostForm, HirerJobPostForm, SearchForm, LoginForm, RegistrationForm
from app.models import User, Job_Post, Job_Offer


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('land_page.html', title="Home")


@app.route('/job_apply', methods=['GET', 'POST'])
@login_required
def job_apply():
    eForm = EmployeeJobPostForm()
    hForm = HirerJobPostForm()
    if eForm.validate_on_submit():
        post = Job_Post(title=hForm.title.data, address=hForm.address.data, salary_price=hForm.salary_price.data,
                        salary_category=hForm.salary_category.data, description=hForm.description.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Successfully Posted the job.')
        return redirect(url_for('index'))
    return render_template('job_apply.html', title="Job Post", eform=eForm, hform=hForm)


@app.route('/job_search', methods=['GET', 'POST'])
@login_required
def job_search():
    search = SearchForm()
    if search.validate_on_submit():
        jobs = Job_Post.query.filter(
            Job_Post.title.contains('{}'.format(search.search.data))).order_by(Job_Post.timestamp.desc())
        return render_template('job_search.html', title='Search Result', sform=search, jobs=jobs)
    return render_template('job_search.html', title='Job Search', sform=search)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('sign_in'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('sign_in.html', title='Sign In', form=form)


@app.route('/sign_out')
def sign_out():
    logout_user()
    return redirect(url_for('index'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    first_name=form.firstname.data, last_name=form.lastname.data, gender=form.gender.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html', title='Sign Up', form=form)
