from app import db
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.jobs.forms import JobPostForm, SearchForm
from app.models import User, Job, Works


jobs = Blueprint('jobs', __name__)


@jobs.route('/job_post', methods=['GET', 'POST'])
@login_required
def job_post():
    form = JobPostForm()
    if form.validate_on_submit():
        pass
    else:
        return render_template('job_post.html', form=form)


@jobs.route('/job_search', methods=['GET', 'POST'])
@login_required
def job_search():
    search = SearchForm()
    if search.validate_on_submit():
        if search.category.data == 'Offer':
            pass
            # jobs = Job_Post.query.filter(
            #   Job_Post.title.contains('{}'.format(search.search.data))).order_by(Job_Post.timestamp.desc())
        else:
            pass
            # jobs = Job_Offer.query.filter(
            #   Job_Offer.job_type.contains('{}'.format(search.search.data))).order_by(Job_Offer.timestamp.desc())
        return render_template('job_search.html', title='Search Result', sform=search, jobs=jobs)
    return render_template('job_search.html', title='Job Search', sform=search)
