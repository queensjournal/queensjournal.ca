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

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    # THE django-mobile HAS TO BE FIRST IN THIS LIST OR IT WON'T WORK
    'django_mobile.loader.Loader',
    #########################################
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    'django_mobile.context_processors.flavour',
    "stories.context_processors.media_url",
    # required to render correct templates (grappelli+admin-tools or grappelli "standalone")
    #"grappelli.context_processors.admin_template_path",
)

MIDDLEWARE_CLASSES = (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
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
    'django.contrib.markup',
    'django.contrib.staticfiles',
    
    
    #'comments',
    #'comment_utils',
    
    #'debug_toolbar',

    # Dependencies
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

COMPRESS = False

WIKI_REQUIRES_LOGIN = True