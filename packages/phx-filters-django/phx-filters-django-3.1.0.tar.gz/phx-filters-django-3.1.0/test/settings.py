"""
Minimal Django settings, just enough to get unit tests to run.
"""
from uuid import uuid4

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

DEBUG = True
INSTALLED_APPS = ['test.app']
SECRET_KEY = uuid4().hex
