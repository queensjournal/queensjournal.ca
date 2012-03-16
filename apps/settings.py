import os

DJANGO_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(DJANGO_ROOT)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('tyler', 'tyler@tylerball.net'),
)

MANAGERS = ADMINS

AUTH_USER_PROFILE = 'structure.Author'

TIME_ZONE = 'America/Toronto'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False
USE_L10N = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static/')

TEMPLATE_DIRS = (
    os.path.join(DJANGO_ROOT, "templates/"),
)

STATICFILES_DIRS = (
    os.path.join(DJANGO_ROOT, 'static/'),
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

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    'django_mobile.context_processors.flavour',
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
    'pagination.middleware.PaginationMiddleware',

    'django_mobile.middleware.SetFlavourMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.staticfiles',

    # Dependencies
    'pipeline',
    'django_mobile',
    'haystack',
    'custom',
    'typogrify',
    'imagekit',
    'tagging',
    'shorturls',
    'oembed',
    'disqus',
    'pagination',
    'south',

    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'archive',
    'polls',
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

    # Staff apps
    'staff',
    'staff.requests',
    'staff.wiki',
)

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
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

from settings_local import *

from settings_pipeline import *
PIPELINE_ROOT = os.path.join(DJANGO_ROOT, 'static/')

if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
