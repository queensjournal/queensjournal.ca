# JOURNAL DEPLOYMENT SETTINGS
# These are for reference/or in case the server ever blows up.
# You'll need to put this on the server and rename it to settings_local.py and fill in the Database section, which is left blank for security reasons.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '3781lanru0j_j2',     # Or path to database file if using sqlite3.
        'USER': '3781lanru0j_j2',        # Not used with sqlite3.
        'PASSWORD': 'gESDh2W9rz',# Not used with sqlite3.
        'HOST': '',            # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',            # Set to empty string for default. Not used with sqlite3.
    }
}

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/3781lanru0j/webapps/media2/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://queensjournal.ca/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jqb%^1wtw4#g2ug8w^shcm=&o)$^dx7$os3cnbexpy@607vuwu'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	"/home/3781lanru0j/webapps/journal/templates/"
)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://queensjournal.ca/media/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/3781lanru0j/webapps/media2/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/Users/tyler/Sites/weare.to/templates/static/',
)

AKISMET_API_KEY = 'a749fbcef622'

HAYSTACK_XAPIAN_PATH = '/home/3781lanru0j/webapps/journal/xapian'

# Twitter Authentication info for posting new stories to Twitter
# Visit dev.twitter.com for more info.

TWITTER_CONSUMER_KEY = 'PjgX8fatfPZpni8LfDsw'
TWITTER_CONSUMER_SECRET ='I7ApkCNAAZXzeUw2KdDLbjj33a2kKL7Vj5n2smGq1l4'
TWITTER_ACCESS_TOKEN_KEY ='16619266-pqQxfmoRhVJ0DdTmQGe21F3YuWXaE1cjtc521rj04'
TWITTER_ACCESS_TOKEN_SECRET ='c0i5AX2cGtbvpeJv96FH6viQ9hEBo6COqIk3kFXNM'

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
CACHE_BACKEND = 'memcached://unix:/home/3781lanru0j/memcached.sock'

# Webfaction e-mail settings (no e-mail server on the Django machine)
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'journal'
EMAIL_HOST_PASSWORD = 'weheartgabe'
DEFAULT_FROM_EMAIL = 'server@queensjournal.ca'
SERVER_EMAIL = 'server@queensjournal.ca'

AKISMET_API_KEY = 'a749fbcef622'

SHORT_BASE_URL = "http://qjrnl.net/"
SHORTEN_FULL_BASE_URL = "http://queensjournal.ca/"