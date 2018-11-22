from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.users.forms import LoginForm, RegistrationForm, EditProfile
from app.models import User, Job_Post, Job_Offer


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
        user.contact_number = form.contact_no.data
        user.last_name = form.lastname.data
        user.gender = form.gender.data
        user.email = form.email.data
        user.password = form.password.data
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
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.firstname.data
        current_user.contact_number = form.contact_no.data
        current_user.last_name = form.lastname.data
        current_user.gender = form.gender.data
        current_user.edu_background = form.edu_background.data
        db.session.commit()
        flash('Successfully Edited Profile.', category='success')
        return redirect(url_for('users.home'))
    else:
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.gender.data = current_user.gender
        form.contact_no.data = current_user.contact_number
        form.edu_background.data = current_user.edu_background
        image_file = url_for(
            'static', filename='profile_pics/' + current_user.image_file)
        return render_template('edit_profile.html', title='Edit Profile', form=form, image_file=image_file)


@users.route('/home')
@login_required
def home():
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('home.html', title='Profile', image_file=image_file)
