import os


class Config(object):
    SECRET_KEY = 'samplesecret'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost/iassistdb'.format(
        os.environ.get('PASSWORD'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
