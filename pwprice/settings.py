"""
Django settings for pwprice project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*r5_@7x76=r+%s*+v@_b998dn2+tv!=97te9m$4jlm07ebj65r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwprice'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pwprice.urls'

WSGI_APPLICATION = 'pwprice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

RAKUTEN_APP_ID = "1031991221960309245"
VALUE_TOKEN_ID = "110c2bd9856649678c40168d3a09a0d9d"
YAHOO_S_ID = "dj0zaiZpPXQ4MjlYTUdRZzBOSyZzPWNvbnN1bWVyc2VjcmV0Jng9ZWM-"
YAHOO_S_AF_ID = "http%3a%2f%2fck%2ejp%2eap%2evaluecommerce%2ecom%2fservlet%2freferral%3fsid%3d3159552%26pid%3d882986629%26vc_url%3d"
YAHOO_A_ID = "dj0zaiZpPURLc3hGMmlPRWIzWSZzPWNvbnN1bWVyc2VjcmV0Jng9YmM-"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
SITE_DOMAIN = os.environ.get('', '127.0.0.1:8080')

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
print STATIC_ROOT

STATIC_URL = 'http://'+ SITE_DOMAIN +'/static/'
print STATIC_URL
#STATIC_URL = '/static/'

TEMPLATE_DIRS = (
                 # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
                 # Always use forward slashes, even on Windows.
                 # Don't forget to use absolute paths, not relative paths.
                 'pwprice/template',
                 )
