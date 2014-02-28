import os
from settings import *
# JOURNAL DEPLOYMENT SETTINGS
# These are for reference/or in case the server ever blows up.
# You'll need to put this on the server and rename it to settings_local.py and fill in the Database section, which is left blank for security reasons.

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

MEDIA_URL = '/media/' # TODO change on prod

STATIC_URL = '/static/' # TODO change on prod

SECRET_KEY = '' # TODO Fill on prod

HAYSTACK_XAPIAN_PATH = os.path.join(PROJECT_ROOT, 'xapian/')

# don't package assets in prod
STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'

# Twitter Authentication info for posting new stories to Twitter
# Visit dev.twitter.com for more info.

TWITTER_CONSUMER_KEY = 'TODO'
TWITTER_CONSUMER_SECRET ='TODO'
TWITTER_ACCESS_TOKEN_KEY ='TODO'
TWITTER_ACCESS_TOKEN_SECRET ='TODO'

TWITTER_DEV = False

# MEMCACHED Config
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# short url configuration
SHORT_BASE_URL = "http://qjrnl.net/"
SHORTEN_FULL_BASE_URL = "http://queensjournal.ca/"
