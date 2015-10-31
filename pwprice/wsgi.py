"""
WSGI config for pwprice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import sys
import os
import site

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
site.addsitedir('/usr/local/lib/python2.7/site-packages')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pwprice.pwprice_settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
