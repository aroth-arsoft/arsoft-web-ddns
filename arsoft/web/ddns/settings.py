#!/usr/bin/python
# -*- coding: utf-8 -*-
# kate: space-indent on; indent-width 4; mixedindent off; indent-mode python;

# Django settings for arsoft.web.ddns project.
from arsoft.web.utils import initialize_settings
import os.path

# use initialize_settings from arsoft.web.utils to get the initial settings
# for a Django web application.
initialize_settings(__name__, __file__)

SITE_ID = 1

INSTALLED_APPS.append('django.contrib.admin')
MIDDLEWARE_CLASSES.append('django.contrib.auth.middleware.AuthenticationMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(APP_DATA_DIR, 'ddns.db')
    }
}

DEBUG=True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '}zxYtIXN]A6w~|f!;[\jTl*uN$Dwc/Q;b}CI~P|Jh<|?#keD`>VbxRMFrOZ*9xS'

DEFAULT_TTL = 120
DEFAULT_RRTYPE = 'A'

DNS_SERVER = '127.0.0.1'
DNS_TIMEOUT = 10
DNS_QUERY_SOURCE = '*'
DNS_QUERY_SOURCE_PORT = 0
