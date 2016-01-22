from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'veganuconn',
        'USER': 'veganuconn',
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

DEBUG = False
