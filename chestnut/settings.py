#-*- coding: utf-8 -*-
"""
Django settings for chestnut project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '06*-^&mak)@zcd=6$a&2i$ws&@*lr12s23rl-4-rt697^c#x^w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chestnut',
    'api',
    'common',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'chestnut.urls'

WSGI_APPLICATION = 'chestnut.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chestnut',
        'USER': 'chestnut',
        'PASSWORD': 'chestnut',
        'HOST': 'localhost',

    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {

            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            #'filters': ['special'],
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/','all.log'), #或者直接写路径：'c://logs/all.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/','script.log'), #或者直接写路径：'filename':'c:/logs/request.log''
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/','script.log'), #或者直接写路径：'filename':'c:/logs/script.log'
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'api_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/','api.log'), #或者直接写路径：'filename':'c:/logs/script.log'
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'scripts': { # 脚本专用日志
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'api': { # 脚本专用日志
            'handlers': ['api_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
