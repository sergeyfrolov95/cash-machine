import os


class Base(object):

    # Debug
    DEBUG = False
    TESTING = False

    # Security
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'RlnJ9Du3tPGq1jrCAEMaY3wm1oVop225DIf8wlaVl7eu5XibLN'
    WTF_CSRF_SECRET_KEY = 'IhAvE1a5ReAlLy6SeCrEtE4kEy'
    SECURITY_PASSWORD_SALT = 'IhAvE1a5ReAlLy6SeCrEtE4kEy'

    # Database
    SQLALCHEMY_DATABASE_URI = ''

    # Paths
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    DOMAIN = 'localhost'


# Production configuration class
class Production(Base):

    # Debug
    DEBUG = False
    TESTING = False


# Development configuration class
class Development(Base):

    # Debug
    DEBUG = False
    TESTING = True
