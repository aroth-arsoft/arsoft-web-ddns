#!/usr/bin/python
# -*- coding: utf-8 -*-
# kate: space-indent on; indent-width 4; mixedindent off; indent-mode python;

# Django settings for arsoft.web.ddns project.
from arsoft.web.utils import initialize_settings

# use initialize_settings from arsoft.web.utils to get the initial settings
# for a Django web application.
initialize_settings(__name__, __file__)

SITE_ID = 1

DEBUG=True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '}zxYtIXN]A6w~|f!;[\jTl*uN$Dwc/Q;b}CI~P|Jh<|?#keD`>VbxRMFrOZ*9xS'


