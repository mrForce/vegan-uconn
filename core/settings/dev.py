from .base import *

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8b@qr5-ysu^6v55^zkhd7b@46r^fixvwfg!yqr4whkk@47yv07'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
