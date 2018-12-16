from app import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import enum


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Message(db.Model):
    __tablename__ = 'Messages'
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    jobID = db.Column(db.Integer, db.ForeignKey('Jobs.id'), primary_key=True)
    content = db.Column(db.String(400))
    fromUser = db.Column(db.String(100))
    toUser = db.Column(db.String(120))
    status = db.Column(db.String(120), default="Not Read")
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    messaged_job = db.relationship('Job', back_populates='senders')
    sender = db.relationship('User', back_populates='messaged_jobs')


class Works(db.Model):
    __tablename__ = 'Works'
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    jobID = db.Column(db.Integer, db.ForeignKey('Jobs.id'), primary_key=True)
    ratings = db.Column(db.Integer)
    isAccepted = db.Column(db.Boolean, default=False)
    message = db.Column(db.String(120))
    status = db.Column(db.String(120), default="Not Working Not Read")
    working_start_time = db.Column(db.DateTime)
    comments = db.Column(db.String(64))
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    worked_job = db.relationship('Job', back_populates='workers')
    worker = db.relationship('User', back_populates='worked_jobs')


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,
                         unique=True)
    email = db.Column(db.String(120), unique=True)
    birthDate = db.Column(db.Date)
    password_hash = db.Column(db.String(128))
    contact = db.Column(db.String(20))
    address = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(2))
    isEmployed = db.Column(db.Boolean, default=False)
    image_file = db.Column(
        db.String(120), nullable=False, default='default.png')
    jobPosted = db.relationship('Job', backref='user', lazy='dynamic')
    resumeId = db.Column(db.Integer, db.ForeignKey('Resume.id'))
    worked_jobs = db.relationship('Works', back_populates='worker')
    messaged_jobs = db.relationship('Message', back_populates='sender')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_notif(self):
        n = 0
        for Job in self.jobPosted:
            w = Works.query.filter(Works.jobID == Job.id)
            for worker in w:
                if worker.status == 'Not Working Not Read':
                    n = n + 1
        return n

    def get_messages(self):
        pass

    def get_employer(self):
        w = Works.query.filter(Works.userID == self.id)
        for job in w:
            if job.status == 'Working':
                return job.worked_job.user
        return False

    def get_hired_work(self, page):
        w = Works.query.filter(Works.userID == self.id).filter(
            Works.status == 'Hiring')
        if w.first():
            return w.paginate(per_page=2, page=int(page))
        else:
            return False

    def get_current_work(self):
        w = Works.query.filter(Works.userID == self.id)
        for job in w:
            if job.status == 'Working':
                return job
        jobs = self.jobPosted
        for j in jobs:
            if j.postType == 'Seeker':
                wo = Works.query.filter(Works.jobID == j.id)
                for wor in wo:
                    if wor.status == 'Hiring':
                        return wor
        return False

    def get_job_history(self):
        w = Works.query.filter(Works.userID == self.id)
        jobs = self.jobPosted
        job = []
        for work in w:
            if work.status == "Done Not Read" or work.status == "Done Read":
                job.append(work)
        for j in jobs:
            if j.postType == 'Seeker':
                wo = Works.query.filter(Works.jobID == j.id).first()
                if wo:
                    if wo.status == "Done Not Read" or wo.status == "Done Read":
                        job.append(wo)
        return job

    def get_age(self):
        today = date.today()
        if self.birthDate:
            return today.year - self.birthDate.year - ((today.month, today.day) < (self.birthDate.month, self.birthDate.day))
        else:
            return False

    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Job(db.Model):
    __tablename__ = 'Jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    jobType = db.Column(db.String(64))
    description = db.Column(db.String(500))
    duration = db.Column(db.String(20))
    location = db.Column(db.String(128))
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    salary = db.Column(db.String(20))
    postType = db.Column(db.String(100))
    maxWorker = db.Column(db.Integer)
    userId = db.Column(db.Integer, db.ForeignKey('Users.id'))
    workers = db.relationship('Works', back_populates='worked_job')
    senders = db.relationship('Message', back_populates='messaged_job')

    def notification_count(self):
        w = Works.query.filter(Works.jobID == self.id)
        n = 0
        for worker in w:
            if worker.status == 'Not Working Not Read':
                n = n + 1
            if worker.status == 'Done Not Read':
                n = n + 1
        return n

    def worker_count(self):
        w = Works.query.filter(Works.jobID == self.id)
        n = 0
        for worker in w:
            if worker.status == 'Working':
                n = n + 1
        return n

    def hiring_count(self):
        w = Works.query.filter(Works.jobID == self.id)
        n = 0
        for worker in w:
            if worker.status == 'Hiring':
                n = n + 1
        return n

    def applying_count(self):
        w = Works.query.filter(Works.jobID == self.id)
        n = 0
        for worker in w:
            if worker.status == 'Not Working Read':
                n = n + 1
        return n

    def is_full(self):
        w = Works.query.filter(Works.jobID == self.id)
        n = 0
        for worker in w:
            if worker.status == 'Working':
                n = n + 1
        if n == len(self.workers):
            return True
        else:
            return False

    def __repr__(self):
        return f'Posted by {self.user}.'


class Resume(db.Model):
    __tablename__ = 'Resume'
    id = db.Column(db.Integer, primary_key=True)
    education = db.Column(db.String(200))
    workExperience = db.Column(db.String(400))
    user = db.relationship("User", uselist=False, backref='resume')
