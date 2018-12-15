from app import db
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app.jobs.forms import EmployerPostForm, SeekerPostForm, SearchForm, FeedbackForm, MessageForm
from app.models import User, Job, Works, Message


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
        return redirect(url_for('users.home', username=current_user.username, post_page=1, hired_page=1, history_page=1))
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
        return redirect(url_for('users.home', username=current_user.username, post_page=1, hired_page=1, history_page=1))
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
        return redirect(url_for('users.home', username=current_user.username, post_page=1, hired_page=1, history_page=1))
    else:
        if job.maxWorker is not None:
            form.maxWorker.data = job.maxWorker
        form.title.data = job.title
        form.description.data = job.description
        form.job_type.data = job.jobType
        form.location.data = job.location
        form.salary.data = job.salary
        return render_template('edit_job.html', form=form, title='Edit Job')


@jobs.route('/delete_job/<id>')
def delete_job(id):
    job = Job.query.filter_by(id=id).first()
    w = Works.query.filter(Works.jobID == job.id)
    for work in w:
        if work.status == 'Working':
            work.worker.isEmployed = False
            db.session.delete(work)
        if work.status == 'Hiring':
            j = Job.query.filter(Job.id == work.jobID).first()
            j.user.isEmployed = False
            db.session.delete(work)
    db.session.delete(job)
    db.session.commit()
    flash('Successfully Deleted Job', category='success')
    return redirect(url_for('users.home', username=current_user.username, post_page=1, hired_page=1, history_page=1))


@jobs.route('/job_search/<page>', methods=['GET', 'POST'])
def job_search(page):
    search = SearchForm()
    if search.validate_on_submit():
        return redirect(url_for('jobs.search_result', category=search.category.data, search=search.search.data, page=page))
        # return render_template('job_search.html', title='Search Result', sform=search, jobs=jobs)
    else:
        jobs = Job.query.order_by(
            Job.timeStamp.desc()).paginate(per_page=2, page=int(page))
        return render_template('job_search.html', title='Job Search', sform=search, jobs=jobs, check=True, search=False)


@jobs.route('/job_search/<category>/<search>/<page>', methods=['GET', 'POST'])
def search_result(category, search, page):
    srch = SearchForm()
    if srch.validate_on_submit():
        return redirect(url_for('jobs.search_result', category=srch.category.data, search=srch.search.data, page=page))
    else:
        srch.search.data = search
        srch.category.data = category
        jobs = Job.query.filter(Job.postType == category).filter(
            Job.title.contains(f'{search}')).order_by(Job.timeStamp.desc()).paginate(per_page=2, page=int(page))
        return render_template('job_search.html', title='Search Result', sform=srch, jobs=jobs, c=category, s=search)


@jobs.route('/specific_job/<id>')
@login_required
def specific_job(id):
    job = Job.query.filter_by(id=id).first()
    working = Works.query.filter(Works.jobID == job.id)
    if Works.query.filter(Works.jobID == job.id).filter(Works.userID == current_user.id).first():
        status = True

    else:
        status = False
        for work in working:
            if work.status == 'Not Working Not Read':
                work.status = 'Not Working Read'
    db.session.commit()
    return render_template('specific_job.html', title="Job Info", job=job, status=status, work=working)


@jobs.route('/cancel_apply/<id>/<username>')
@login_required
def cancel_apply(id, username):
    job = Job.query.filter_by(id=id).first()
    user = User.query.filter_by(username=username).first()
    w = Works.query.filter(Works.jobID == job.id).filter(
        Works.userID == user.id).first()
    if w.status == 'Working' or w.status == 'Hiring':
        w.worker.isEmployed = False
    db.session.delete(w)
    db.session.commit()
    flash('Successfully Canceled Request', category='success')
    return redirect(url_for('jobs.specific_job', id=job.id))


@jobs.route('/job_apply/<id>')
@login_required
def job_apply(id):
    w = Works()
    job = Job.query.filter_by(id=id).first()
    user = User.query.filter_by(id=current_user.id).first()
    if Works.query.filter(Works.jobID == job.id).filter(Works.userID == user.id).first():
        flash('You Already Applied for this job!', category='danger')
        return redirect(url_for('jobs.specific_job', id=job.id))
    else:
        w.worked_job = job
        w.worker = current_user
        job.workers.append(w)
        db.session.add(w)
        db.session.commit()
        flash('Applied Successfully please wait for approval!', category='success')
        return redirect(url_for('jobs.specific_job', id=job.id))


@jobs.route('/accept_seeker/<username>/<id>')
@login_required
def accept_seeker(username, id):
    job = Job.query.filter_by(id=id).first()
    user = User.query.filter_by(username=username).first()
    if job.postType == 'Seeker':
        if user.isEmployed:
            flash('You are already Employed!', category='danger')
            return redirect(url_for('jobs.specific_job', id=job.id))
        w = Works.query.filter(Works.jobID == job.id).filter(
            Works.userID == user.id).first()
        w.status = 'Hiring'
        job.user.isEmployed = True
        w.isAccepted = True
        db.session.commit()
        flash('Successfully Accepted Job!', category='success')
        return redirect(url_for('jobs.specific_job', id=job.id))
    else:
        if job.user.isEmployed is False:
            flash('User is already Employed!', category='danger')
            return redirect(url_for('jobs.specific_job', id=job.id))
        w = Works.query.filter(Works.jobID == job.id).filter(
            Works.userID == user.id).first()
        w.status = 'Working'
        user.isEmployed = True
        w.isAccepted = True
        db.session.commit()
        flash('Successfully Accepted User!', category='success')
        return redirect(url_for('jobs.specific_job', id=job.id))


@jobs.route('/job_done/<username>/<id>', methods=['GET', 'POST'])
@login_required
def job_done(username, id):
    form = FeedbackForm()
    job = Job.query.filter(Job.id == id).first()
    if job.postType == 'Employer':
        user = User.query.filter(User.id == job.user.id).first()
    else:
        user = User.query.filter(User.username == username).first()
    if request.method == 'POST' and form.validate_on_submit():
        print(request.form['selected_rating'])
        print(user)
        work = Works.query.filter(Works.jobID == job.id).filter(
            Works.userID == user.id).first()
        work.status = 'Done Not Read'
        work.message = form.message.data
        work.rating = request.form['selected_rating']
        if work.rating:
            db.session.commit()
            flash('Success', category='success')
            return redirect(url_for('jobs.job_done', username=username, id=id))
        else:
            flash('Please rate the User.', category='danger')
            form.message.data = work.message
            return redirect(url_for('jobs.job_done', username=username, id=id))
    else:
        return render_template('feedback.html', form=form, job=job, user=user)


@jobs.route('/message/<page>')
@login_required
def message(page):
    m = Message.query.filter(Message.userID == current_user.id).join(Job).filter(Job.id==Message.jobID).paginate(
        per_page=2, page=int(page))
    return render_template('messages.html', messages=m, title="Messages")

@jobs.route('/test')
def test123():
    s = current_user.get_job_history(1)
    m = db.session.query(Works).filter(Works.userID == current_user.id).join(Message, Message.jobID == Works.jobID).all()
    print(m)
    return render_template('test.html', message=m, title="TEST")

@jobs.route('/message/<id>/<username>', methods=['GET', 'POST'])
@login_required
def specific_message(id, username):
    u = User.query.filter(User.username == username).first()
    m = Message.query.filter(Message.jobID == id).filter(
        Message.userID == user.id).first()
    m.status = 'Read'
    db.session.commit()
    return render_template('specific_message.html', message=m, title="Specific Message")


@jobs.route('/create_message/<id>/<username>', methods=['GET', 'POST'])
@login_required
def create_message(id, username):
    form = MessageForm()
    j = Job.query.filter(Job.id==id).first()
    if request.method == 'POST' and form.validate_on_submit():
        m = Message()
        m.messaged_job = j
        m.sender = current_user
        j.senders.append(m)
        m.content = form.content.data
        m.fromUser = current_user
        m.toUser = j.user
        db.session.commit()
        flash('Message Sent!', category='success')
        return redirect(url_for('users.home', username=current_user.username, post_page=1, hired_page=1, history_page=1))
    else:
        return render_template('create_message.html', form=form, title="Message", user=current_user, job=j)

