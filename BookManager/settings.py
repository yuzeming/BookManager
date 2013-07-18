# Django settings for BookManager project.

PASSWORD = "12345"

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'book.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ainfeswf3r39rf093289fweml'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

ROOT_URLCONF = 'BookManager.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'BookManager.wsgi.application'

import os
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'BookManager'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
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

DATE_FORMAT = "Y-m-d"

noimg = """
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
Ba2XARMmfsP/2Q=="""