from app import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import enum


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Works(db.Model):
    __tablename__ = 'Works'
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    jobID = db.Column(db.Integer, db.ForeignKey('Jobs.id'), primary_key=True)
    ratings = db.Column(db.Integer)
    isAccepted = db.Column(db.Boolean, default=False)
    message = db.Column(db.String(120))
    status = db.Column(db.String(120), default="Not Working")
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

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    title = db.Column(db.String(24))
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

    def __repr__(self):
        return f'Posted by {self.user}.'


class Resume(db.Model):
    __tablename__ = 'Resume'
    id = db.Column(db.Integer, primary_key=True)
    education = db.Column(db.String(200))
    workExperience = db.Column(db.String(400))
    user = db.relationship("User", uselist=False, backref='resume')
