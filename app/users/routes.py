from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.users. utils import save_picture

from app.users.forms import LoginForm, RegistrationForm, EditProfile, EditIMG
from app.models import User, Job, Works


users = Blueprint('users', __name__)


@users.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.first_name = form.firstname.data
        user.last_name = form.lastname.data
        user.gender = form.gender.data
        user.email = form.email.data
        user.contact = form.contact_no.data
        user.password = form.password.data
        user.address = form.location.data
        date = form.birthDate.data.split('/')
        year = date.pop()
        date.insert(0, year)
        newDate = ""
        for i in date:
            newDate += i + "-"
        newDate = newDate[:-1]
        user.birthDate = newDate
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', category='success')
        return redirect(url_for('users.sign_in'))
    return render_template('sign_up.html', title='Sign Up', form=form)


@users.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password', category='danger')
            return redirect(url_for('users.sign_in'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('users.home')
        return redirect(next_page)
    return render_template('sign_in.html', title='Sign In', form=form)


@users.route('/sign_out')
def sign_out():
    logout_user()
    return redirect(url_for('users.sign_in'))


@users.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    if form.validate_on_submit() and request.method == 'POST':
        current_user.first_name = form.firstname.data
        current_user.last_name = form.lastname.data
        current_user.contact = form.contact_no.data
        current_user.email = form.email.data
        current_user.gender = form.gender.data
        current_user.address = form.location.data
        db.session.commit()
        flash('Successfully Edited Profile.', category='success')
        return redirect(url_for('users.home'))
    else:
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.gender.data = current_user.gender
        form.email.data = current_user.email
        form.location.data = current_user.address
        form.gender.data = current_user.gender
        form.contact_no.data = current_user.contact
        return render_template('edit_profile.html', title='Edit Profile', form=form)


@users.route('/home/', methods=['POST', 'GET'])
@login_required
def home():
    form = EditIMG()
    job_posted = Job.query.filter(Job.userId == current_user.id).all()
    current_age = current_user.get_age()
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    if form.validate_on_submit and request.method == 'POST':
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            db.session.commit()
            flash('Changed Profile Picture.', category='success')
        else:
            flash('Failed', category='danger')
        return redirect(url_for('users.home'))
    else:
        return render_template('home.html', title='Profile', form=form, image_file=image_file, age=current_age, job_posted=job_posted)


@users.route('/uploadIMG', methods=['POST'])
def uploadIMG():
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
