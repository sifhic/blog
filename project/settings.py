"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import errno

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_NAME = 'blog'
INSTANCE_DIR = '/tmp/' + PROJECT_NAME + '/'

# TODO Warn if instance directory doesn't exist
def create_dirs(instance_dir):
    if not os.path.exists(os.path.dirname(instance_dir)):
        try:
            os.makedirs(os.path.dirname(instance_dir))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


create_dirs(INSTANCE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y#9r1u$hxrm!u*%^04ia^+tzrh3c7mxgrf29!ln-*20xo()x4$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'blog.apps.BlogConfig',
    'admin.apps.AdminConfig',
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'authentication',
    'sorl.thumbnail',
    'newsletter',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'authentication.middleware.AuthenticationRequiredMiddleware',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            #'TEMPLATE_DEBUG':True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

AUTH_USER_MODEL = 'authentication.User'

ADMIN_LOGIN = 'admin'
ADMIN_PASSWORD = 'pbkdf2_sha256$30000$37vfsTPxkZ2N$5JCLjrA2WWPSnqP2oHul9JFswSvHeSOLGhxw9YL6p4E=' # brian123
# pbkdf2_sha256$120000$RWQiuEruqUVc$fAbFOwuFNPMkOwaaHbpQDnfgVFx8Q1GemD+JGvusogY= 12345

AUTHENTICATION_BACKENDS = [
    'authentication.backends.settings.SettingsBackend',
    'authentication.backends.username_or_email.UsernameEmailBackend'
]


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


INDEX_URL = '/'
LOGIN_URL = '/login/'

LOGIN_DEFAULT_PERMISSIVE = True

LOGIN_DEFAULT_EXEMPT_URLS = (
    #  LOGIN_URL.lstrip('/'),  # might be needed if not default permissive
    'admin/',
)


LOGIN_SESSION_REDIRECT_HOME_URLS = (
    'signup/',
    'reset/',
    'password_reset/',
    'account_activation_sent/',
)


# used for mailer links
# todo this should be consistent with the site
PROTOCOL = 'http'
HOST = 'localhost'
PORT = 8000


if DEBUG:
    # EMAIL_HOST = 'smtp.mailtrap.io'
    # EMAIL_HOST_USER = '0214920fb35621'
    # EMAIL_HOST_PASSWORD = '6239ad1f8c3275'
    # EMAIL_PORT = '2525'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'sendgrid_username'
    EMAIL_HOST_PASSWORD = 'sendgrid_password'
    EMAIL_USE_TLS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(INSTANCE_DIR, 'static')
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static_libs'),
]
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(INSTANCE_DIR, 'media')
MEDIA_URL = '/media/'


def skip_static_requests(record):
    if record.args[0].startswith('GET /static/'): # bug HTTPStatus.BAD_REQUEST
        return False
    return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'skip_static_requests': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_static_requests
        }
    },
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(INSTANCE_DIR, PROJECT_NAME+'.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'verbose'

        },
        'django.server': {
            'level': 'INFO',
            # 'filters': ['skip_static_requests'],  # <- ...with one change
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'blog': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        },
        'authentication': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG'
        }

    },
}
