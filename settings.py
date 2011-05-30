# Django settings for journal project.
# Import settings_local.py for site-specific vars
# (keeps everything nice and tidy in the repository!)
from settings_local import *
import os

ADMINS = (
	('tyler', 'tyler@tylerball.net'),
)

MANAGERS = ADMINS

AUTH_USER_PROFILE = 'structure.Author'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
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
	"stories.context_processors.media_url",
	
	# required to render correct templates (grappelli+admin-tools or grappelli "standalone")
	#"grappelli.context_processors.admin_template_path",
)

MIDDLEWARE_CLASSES = (
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
	'django.contrib.redirects',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	#'django.contrib.comments',
	'django.contrib.humanize',
	
	
	#'comments',
	#'comment_utils',

	# Dependencies
	
	'haystack',
	'custom',
	'dependencies.template_utils',
	'typogrify',
	'imagekit',
	'tagging',
	'shorturls',
	'oembed',
	#'djcelery',
	#'ghettoq',
	#'djkombu',
	'disqus',
	
	#'grappelli',
	
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	'django.contrib.admindocs',
	'django.contrib.flatpages',
	'polls',
	'stories',
	'structure',
	'sidebars',
	'sidelinks',
	'blog',
	'staff',
	'images',
	'inlines',
	'galleries',
	'masthead',
	'video',
)

SHORTEN_MODELS = {
	's': 'stories.story',
	'b': 'blog.entry',
	'v': 'video.video',
	}

SHORT_BASE_URL = "http://qjrnl.net/"
SHORTEN_FULL_BASE_URL = "http://queensjournal.ca/"

DISQUS_API_KEY = "ZbgAB94X7tUepMQU4tbmkm89bxzpSokmlV56hNIoh0UjEnfel4TrevUtZoAwU035"
DISQUS_WEBSITE_SHORTNAME = "queensjournal"

HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15

# Setting for CELERY.
CARROT_BACKEND = "ghettoq.taproot.Database"