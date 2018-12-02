from app import db
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.jobs.forms import EmployerPostForm, SeekerPostForm, SearchForm
from app.models import User, Job, Works


jobs = Blueprint('jobs', __name__)


@jobs.route('/job_post', methods=['GET', 'POST'])
@login_required
def job_post():
    eform = EmployerPostForm()
    sform = SeekerPostForm()
    post = Job()
    if sform.validate_on_submit():
        post.title = sform.stitle.data
        post.description = sform.sdescription.data
        post.jobType = sform.sjob_type.data
        post.location = sform.slocation.data
        post.salary = sform.ssalary.data
        post.user = current_user
        post.postType = 'Seeker'
        db.session.add(post)
        db.session.commit()
        flash('Successfully posted job seeker!', category='success')
        return redirect(url_for('users.home'))
    if eform.validate_on_submit():
        post.title = eform.title.data
        post.postType = 'Employer'
        post.description = eform.description.data
        post.jobType = eform.job_type.data
        post.location = eform.location.data
        post.salary = eform.salary.data
        post.maxWorker = eform.maxWorker.data
        post.user = current_user
        db.session.add(post)
        db.session.commit()
        flash('Successfully posted job employer!', category='success')
        return redirect(url_for('users.home'))
    else:
        return render_template('job_post.html', title='Job Post', eform=eform, sform=sform)


@jobs.route('/edit_job/<id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    job = Job().query.filter_by(id=id).first()
    form = EmployerPostForm()
    if form.validate_on_submit():
        if form.maxWorker.data:
            job.maxWorker = form.maxWorker.data
        job.title = form.title.data
        job.description = form.description.data
        job.jobType = form.job_type.data
        job.location = form.location.data
        job.salary = form.salary.data
        db.session.commit()
        flash('Successfully Edited Job', category='success')
        return redirect(url_for('users.home'))
    else:
        if job.maxWorker is not None:
            form.maxWorker.data = job.maxWorker
        form.title.data = job.title
        form.description.data = job.description
        form.job_type.data = job.jobType
        form.location.data = job.location
        form.salary.data = job.salary
        return render_template('edit_job.html', form=form, title='Edit Job')


@jobs.route('/delete_job/<id>', methods=['POST', 'GET'])
def delete_job(id):
    job = Job.query.filter_by(id=id).first()
    db.session.delete(job)
    db.session.commit()
    flash('Successfully Deleted Job', category='success')
    return redirect(url_for('users.home'))


@jobs.route('/job_search', methods=['GET', 'POST'])
@login_required
def job_search():
    search = SearchForm()
    if search.validate_on_submit():
        if search.category.data == 'Offer':
            pass
            # jobs = Job.query.filter(
            #   Job.title.contains('{}'.format(search.search.data))).order_by(Job.timetamp.desc())
        else:
            pass
            # jobs = Job_Offer.query.filter(
            #   Job_Offer.job_type.contains('{}'.format(search.search.data))).order_by(Job_Offer.timestamp.desc())
        return render_template('job_search.html', title='Search Result', sform=search, jobs=jobs)
    else:
        jobs = Job.query.order_by(Job.timeStamp.desc())
        return render_template('job_search.html', title='Job Search', sform=search, jobs=jobs)


@jobs.route('/specific_job/<id>', methods=['GET', 'POST'])
@login_required
def specific_job(id):
    job = Job.query.filter_by(id=id).first()
    return render_template('specific_job.html', title="Job Info", job=job)


@jobs.route('/job_apply/<id>', methods=['POST', 'GET'])
@login_required
def job_apply(id):
    w = Works()
    job = Job.query.filter_by(id=id).first()
    user = User.query.filter_by(id=current_user.id).first()
    for attribute in job.workers:
        if attribute.worker.id == user.id:
            flash(
                'You already applied to this job please wait for approval.', category='danger')
            return redirect(url_for('users.home'))
    w.worked_job = job
    w.worker = current_user
    job.workers.append(w)
    db.session.add(w)
    db.session.commit()
    flash('Applied Successfully please wait for approval!', category='success')
    return redirect(url_for('users.home'))


@jobs.route('/accepted/<id>')
def accept():
    pass
