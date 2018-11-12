from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.forms import EmployeeJobPostForm, HirerJobPostForm, SearchForm, LoginForm, RegistrationForm, EditProfile
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


@app.route('/job_post', methods=['GET', 'POST'])
@login_required
def job_post():
    eForm = EmployeeJobPostForm()
    hForm = HirerJobPostForm()
    if eForm.validate_on_submit():
        post = Job_Offer()
        post.job_type = eForm.job_type.data
        post.contact = eForm.contact.data
        post.description = eForm.description.data
        post.author = current_user
        db.session.add(post)
        db.session.commit()
        flash('Successfully Posted the job.', category='success')
        return redirect(url_for('home'))
    if hForm.validate_on_submit():
        post = Job_Post()
        post.title = hForm.title.data
        post.address = hForm.address.data
        post.salary_price = hForm.salary_price.data
        post.salary_category = hForm.salary_category.data
        post.description = hForm.description.data
        post.author = current_user
        db.session.add(post)
        db.session.commit()
        flash('Successfully Posted the job.', category='success')
        return redirect(url_for('home'))
    return render_template('job_post.html', title="Job Post", eform=eForm, hform=hForm)


@app.route('/job_search', methods=['GET', 'POST'])
@login_required
def job_search():
    search = SearchForm()
    if search.validate_on_submit():
        if search.category.data == 'Offer':
            jobs = Job_Post.query.filter(
                Job_Post.title.contains('{}'.format(search.search.data))).order_by(Job_Post.timestamp.desc())
        else:
            jobs = Job_Offer.query.filter(
                Job_Offer.job_type.contains('{}'.format(search.search.data))).order_by(Job_Offer.timestamp.desc())
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
            flash('Invalid Username or Password', category='danger')
            return redirect(url_for('sign_in'))
        flash('Successfully Logged in.', category='success')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('sign_in.html', title='Sign In', form=form)


@app.route('/sign_out')
def sign_out():
    logout_user()
    flash('Signed Out!', category='success')
    return redirect(url_for('sign_in'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.first_name = form.firstname.data
        user.contact_number = form.contact_no.data
        user.last_name = form.lastname.data
        user.gender = form.gender.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', category='success')
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html', title='Sign Up', form=form)


@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='Profile')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit() and request.method == 'POST':
        user.first_name = form.firstname.data
        user.contact_number = form.contact_no.data
        user.last_name = form.lastname.data
        user.gender = form.gender.data
        user.edu_background = form.edu_background.data
        db.session.add(user)
        db.session.commit()
        flash('Successfully Edited Profile.', category='success')
        return redirect(url_for('home'))
    else:
        form.firstname.data = user.first_name
        form.lastname.data = user.last_name
        form.gender.data = user.gender
        form.contact_no.data = user.contact_number
        form.edu_background.data = user.edu_background
        return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/job_post/<id>', methods=['GET', 'POST'])
def specific_job_post(id):
    job_post = Job_Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        return redirect('home')
    else:
        return render_template('specific_job_post.html', job_post=job_post, title='Job Post')


@app.route('/job_offer/<id>', methods=['GET', 'POST'])
def specific_job_offer(id):
    job_offer = Job_Offer.query.filter_by(id=id).first()
    if request.method == 'POST':
        return redirect('home')
    else:
        return render_template('specific_job_offer.html', job_offer=job_offer, title='Job Offer')
