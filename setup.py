#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='arsoft-web-ddns',
		version='1.6',
		description='Simple dynamic DNS service',
		author='Andreas Roth',
		author_email='aroth@arsoft-online.com',
		url='http://www.arsoft-online.com/',
		packages=['arsoft.web.ddns'],
		scripts=['arsoft-ddns'],
		data_files=[
            ('/etc/arsoft/web/ddns/config', ['config/settings.py']),
            ('/etc/arsoft/web/ddns/static', ['arsoft/web/ddns/static/main.css']),
            ('/usr/lib/arsoft-web-ddns', ['manage.py']),
            ]
		)
