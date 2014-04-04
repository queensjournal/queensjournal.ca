import os
import sys
import django.conf.global_settings as DEFAULT_SETTINGS

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
PROJECT_NAME = 'journal'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('tyler', 'tyler@tylerball.net'),
)

MANAGERS = ADMINS

AUTH_USER_PROFILE = 'authors.Author'

TIME_ZONE = 'America/Toronto'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False
USE_L10N = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'served/media/')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'served/static/')

# PIPELINE storage
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_YUGLIFY_BINARY = 'node_modules/.bin/yuglify'
PIPELINE_COMPASS_BINARY = '/usr/bin/env bundle exec compass'
PIPELINE_COMPASS_ARGUMENTS = '-c ' + os.path.join(PROJECT_ROOT, 'compass.rb')
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE_UGLIFYJS_BINARY = os.path.join(PROJECT_ROOT,
    'node_modules/.bin/uglifyjs')

PIPELINE_COFFEE_SCRIPT_BINARY = os.path.join(PROJECT_ROOT,
    'node_modules/.bin/coffee')
PIPELINE_COMPILERS = (
    'pipeline_compass.compass.CompassCompiler',
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
)


# devdata options
PATH_TO_DEVDATA = os.path.join(PROJECT_ROOT, 'devdata')
DUMBO_DATA_DIR = PATH_TO_DEVDATA
RSYNC_OPTIONS = '--recursive --links --times --omit-dir-times --verbose \
    --delete --exclude=example* --exclude=*cache*'
DUMBO_RSYNC_OPTIONS = RSYNC_OPTIONS

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates/"),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    # THE django-mobile HAS TO BE FIRST IN THIS LIST OR IT WON'T WORK
    'django_mobile.loader.Loader',
    #########################################
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django_mobile.context_processors.flavour',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django_mobile.middleware.MobileDetectionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',

    'django_mobile.middleware.SetFlavourMiddleware',
)

ROOT_URLCONF = 'journal.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.staticfiles',

    # Dependencies
    'haystack',
    'pipeline',
    'django_mobile',
    'custom',
    'typogrify',
    'imagekit',
    'tagging',
    'shorturls',
    'oembed',
    'disqus',
    'pagination',
    'south',
    'bento',
    'selectable',
    'solo',

    'utils',

    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'config',
    'front',
    'issues',
    'archive',
    'sections',
    'authors',
    'stories',
    'structure',
    'sidebars',
    'sidelinks',
    'blog',
    'images',
    'inlines',
    'galleries',
    'masthead',
    'video',
)

SOUTH_MIGRATION_MODULES = {
    'bento': 'migrations.bento',
}

SHORTEN_MODELS = {
    's': 'stories.story',
    'b': 'blog.entry',
    'v': 'video.video',
    'g': 'galleries.gallery',
    }

DISQUS_API_KEY = "ZbgAB94X7tUepMQU4tbmkm89bxzpSokmlV56hNIoh0UjEnfel4TrevUtZoAwU035"
DISQUS_WEBSITE_SHORTNAME = "queensjournal"

HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15

AKISMET_API_KEY = 'a749fbcef622'

WIKI_REQUIRES_LOGIN = True

LOGGING = {
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
     },
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Uses django-discover-runner test discovery
TEST_RUNNER = "discover_runner.DiscoverRunner"
TEST_DISCOVER_TOP_LEVEL = PROJECT_ROOT

HAYSTACK_XAPIAN_PATH = os.path.join(PROJECT_ROOT, 'xapian/')

# Run tests in sqllite
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory',
        },
    }

    PIPELINE = True
    STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'

    SECRET_KEY = 'test_testsdfaklsgag4t345h4h3ergs24394g4rg49'

    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'

    # Don't bother with haystack during tests
    HAYSTACK_SEARCH_ENGINE = 'dummy'
else:
    from journal.settings_local import *

from journal.settings_pipeline import *

PIPELINE_ROOT = os.path.join(PROJECT_ROOT, 'static/')
