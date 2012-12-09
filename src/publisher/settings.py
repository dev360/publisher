from os.path import join as pjoin, dirname, abspath
import logging, sys

gettext = lambda s: s


#
# Sys paths
#
PROJ_ROOT = abspath(dirname(__file__))
lib_path = pjoin(PROJ_ROOT, 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

LOG_FILENAME = pjoin(PROJ_ROOT, 'log', 'publisher.log')
LOG_LEVEL = logging.DEBUG



TIME_ZONE = 'America/New_York'
SITE_ID = 1

# Localization settings
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = USE_I18N

#
# Paths to media/static dirs
#
MEDIA_ROOT = pjoin(PROJ_ROOT, 'media')
STATIC_ROOT = pjoin(PROJ_ROOT, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    pjoin(PROJ_ROOT,'static_files'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


ADMIN_MEDIA_PREFIX = '/media/admin/'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'core.context_processors.global_settings',
)

ROOT_URLCONF = 'publisher.urls'

TEMPLATE_DIRS = (
    pjoin(PROJ_ROOT, 'templates'),
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'devserver',
    'jstools',
    'registration',
    'shrink',
    'south',

    'api',
    'auth',
    'core',
    'utils',

    'storages',
    'debug_toolbar',
)

LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_ACTIVATION_DAYS = 30

LANGUAGES = (
    ('en', gettext('English')),
)


LOGIN_REDIRECT_URL = '/profile/'

SITE_NAME = 'publisher'

from settingslocal import *

# Set debug according to the
# environment we are in.
DEBUG = True if ENVIRONMENT == 'dev' else False
TEMPLATE_DEBUG = DEBUG

USE_CDN = False if ENVIRONMENT == 'dev' else True

MEDIA_URL = '{0}/media/'.format(BASE_URL)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = '1VNS318E3TMK6DMHF982'
AWS_SECRET_ACCESS_KEY = 'kFEpGXI8YGvEDcsuSTsQsb/w1daoP1EiRL9NY350'
AWS_STORAGE_BUCKET_NAME = 'publisherapp'

# see http://developer.yahoo.com/performance/rules.html#expires
AWS_HEADERS = {
    'Expires': 'Thu, 15 Apr 2010 20:00:00 GMT',
    'Cache-Control': 'max-age=86400',
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}
INTERNAL_IPS = ('127.0.0.1',)
