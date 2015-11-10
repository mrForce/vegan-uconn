from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'veganuconn',
        'USER': 'veganuconn',
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEBUG = True
