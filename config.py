class BaseConfig(object):
    pass


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True # suppress warning
