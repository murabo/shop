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
    'pwprice',
    'templatetag_handlebars'
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
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'pwprice',
        'USER': 'root',
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
VALUE_TOKEN_ID = "1-6bd1060df985e94c90462ae569768554"
#YAHOO_S_ID = "dj0zaiZpPXQ4MjlYTUdRZzBOSyZzPWNvbnN1bWVyc2VjcmV0Jng9ZWM-"
YAHOO_S_ID = "dj0zaiZpPTFSYmhwQTFLZHAwWSZzPWNvbnN1bWVyc2VjcmV0Jng9NTI-"
YAHOO_S_AF_ID = "http%3a%2f%2fck%2ejp%2eap%2evaluecommerce%2ecom%2fservlet%2freferral%3fsid%3d3161331%26pid%3d882992162%26vc_url%3d"
YAHOO_A_ID = "dj0zaiZpPURLc3hGMmlPRWIzWSZzPWNvbnN1bWVyc2VjcmV0Jng9YmM-"
MOSHIMO_A_ID = 431508
MOSHIMO_URL = "http://c.af.moshimo.com/af/c/click?a_id=%s&p_id=54&pc_id=54&pl_id=616" % MOSHIMO_A_ID

VC_Y_A_URL = "http://ck.jp.ap.valuecommerce.com/servlet/referral?sid=3161331&pid=882992162&"
RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20140222?"
RAKUTEN_A_API_URL = "https://app.rakuten.co.jp/services/api/AuctionItem/Search/20130110?"
VALUE_API_URL   = "http://webservice.valuecommerce.ne.jp/productdb/search?"
YAHOO_S_URL = "http://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?"
YAHOO_A_URL = "http://auctions.yahooapis.jp/AuctionWebService/V2/search?"

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
#TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',)
