from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,
                         unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(2))
    edu_background = db.Column(db.String(50))
    image_file = db.Column(
        db.String(120), nullable=False, default='default.png')
    job_posts = db.relationship('Job_Post', backref='author', lazy='dynamic')
    job_offers = db.relationship('Job_Offer', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Job_Post(db.Model):
    __tablename__ = 'JobPosts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    address = db.Column(db.String(50))
    salary_price = db.Column(db.Integer)
    salary_category = db.Column(db.String(5))
    contact_details = db.Column(db.String(20))
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return 'Job Post {}'.format(self.title)


class Job_Offer(db.Model):
    __tablename__ = 'JobOffers'
    id = db.Column(db.Integer, primary_key=True)
    job_type = db.Column(db.String(100))
    contact = db.Column(db.String(50))
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return 'Job Offer {}'.format(self.title)
