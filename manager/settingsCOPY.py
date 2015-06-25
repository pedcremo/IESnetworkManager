# Django settings for manager project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os

#APPLICATION_DIR= os.path.split(os.path.abspath(__file__))[0]
APPLICATION_DIR= os.path.split(os.path.abspath(os.path.split(os.path.abspath(__file__))[0]))[0]

ADMINS = (
    # ('Pere Crespo', 'pedcremo@iestacio.com'),
)

MANAGERS = ADMINS

# Google APPS auth settings. Use google apps accounts in order to authenticate in this django application
GAPPS_USERNAME = 'xxxxxx'
GAPPS_DOMAIN = 'iestacio.com'
GAPPS_PASSWORD = 'xxxxxx'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ies_network',                      # Or path to database file if using sqlite3.
        'USER': 'xxxx',                      # Not used with sqlite3.
        'PASSWORD': 'xxxxxxxx',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#Firewall prefix
FW_PREFIX = '46006100'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ca-es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = '/Users/perecrespomolina/Dropbox/IESnetworkManager/manager/aules/media'
#MEDIA_ROOT = '/home/usuari/Dropbox/IESnetworkManager/manager/aules/media'
MEDIA_ROOT =  os.path.join( APPLICATION_DIR,"aules/media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT =  os.path.join( APPLICATION_DIR,"aules/static")
#STATIC_ROOT = '/Users/perecrespomolina/Dropbox/IESnetworkManager/manager/aules/static'
#STATIC_ROOT = '/home/usuari/Dropbox/IESnetworkManager/manager/aules/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
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
SECRET_KEY = 'bf_l5$w!#n0uw%)j67muo@ubqw_zsy+v#eq-qg$nxn&amp;t=rt^99'

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
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'manager.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'manager.wsgi.application'

#STATIC_ROOT =  os.path.join( APPLICATION_DIR,"/images")

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'/home/usuari/Dropbox/IESnetworkManager/manager/templates',
    os.path.join( APPLICATION_DIR,"templates"),
    #'/Users/perecrespomolina/Dropbox/IESnetworkManager/manager/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'aules',
    'proxylog', #Per monitoritzar habits de navegacio
    
)

AUTHENTICATION_BACKENDS = (
    'aules.google_auth.GoogleAppsBackend',
    'django.contrib.auth.backends.ModelBackend',	
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
