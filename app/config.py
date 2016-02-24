class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True # suppress warning
    SECURITY_POST_LOGIN_VIEW = 'index'
    SECURITY_UNAUTHORIZED_VIEW = 'forbidden'
    MIN_PASSWORD_LENGTH = 8


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = 'nHCv7L1pVqAU%5nf64(qDsuTAFLl@me4DPu*lN%3ZDdok22FP6ok#Y7Tb^o8ctxp'
    SQLALCHEMY_DATABASE_URI = 'something postgres'
