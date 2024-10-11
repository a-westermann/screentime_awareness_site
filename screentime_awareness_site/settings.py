"""
Django settings for screentime_awareness_site project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
config = None
if os.path.isfile('config.json'):
    config = open('config.json').read()
    SECRET_KEY = json.loads(config)['DJANGO_SECRET_KEY']
else:
    SECRET_KEY = ['django-secret-key-klasdjflkxicjoliweujlki2j3lkjs']
DEBUG = config is None
print(f'DEBUG MODE = {DEBUG}')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 15
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG

ALLOWED_HOSTS = ['18.222.1.149',  # gobeyondthescreen.org aws ec2 instance public
                 'gobeyondthescreen.org',
                 'www.gobeyondthescreen.org',
                 '172.31.7.125',  # private ip, prob not needed
                 '192.168.1.29',
                 '192.168.1.229',
                 '192.168.1.87',
                 '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'screentime_awareness_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'screentime_awareness_site.wsgi.application'

# MEDIA_ROOT = os.path.join(os.curdir, 'media')
MEDIA_ROOT = "/screentime_awareness_site/media/"
MEDIA_URL = "/media/"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SESSION_COOKIE_AGE = 30 * 60  # expire session after 30 minutes of no new cookies

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Static Root is not really needed. collectstatic is used to collect all static files from
# 3rd party libraries, etc into the folder that the server will serve from
# STATIC_ROOT = '/home/ubuntu/screentime_awareness_site/'
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')
                    ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = 'support@gobeyondthescreen.org'
SERVER_EMAIL = 'support@gobeyondthescreen.org'
EMAIL_USE_TLS = True
file = json.loads(open('email_pw').read())
EMAIL_HOST = file['email_host']
EMAIL_PORT = file['port']
EMAIL_HOST_USER = file['email_host_user']
EMAIL_HOST_PASSWORD = file['email_host_password']

