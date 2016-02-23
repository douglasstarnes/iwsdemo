class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True # suppress warning
    SECURITY_POST_LOGIN_VIEW = 'home'
    MIN_PASSWORD_LENGTH = 8


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    DEBUG = True
