from app import db
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.jobs.forms import EmployeeJobPostForm, HirerJobPostForm, SearchForm
from app.models import User, Job_Post, Job_Offer


jobs = Blueprint('jobs', __name__)


@jobs.route('/job_post/<id>', methods=['GET', 'POST'])
@login_required
def specific_job_post(id):
    job_post = Job_Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        return redirect('home')
    else:
        return render_template('specific_job_post.html', job_post=job_post, title='Job Post')


@jobs.route('/job_offer/<id>', methods=['GET', 'POST'])
@login_required
def specific_job_offer(id):
    job_offer = Job_Offer.query.filter_by(id=id).first()
    if request.method == 'POST':
        return redirect('home')
    else:
        return render_template('specific_job_offer.html', job_offer=job_offer, title='Job Offer')


@jobs.route('/job_post', methods=['GET', 'POST'])
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
        return redirect(url_for('users.home'))
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
        return redirect(url_for('users.home'))
    return render_template('job_post.html', title="Job Post", eform=eForm, hform=hForm)


@jobs.route('/job_search', methods=['GET', 'POST'])
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
