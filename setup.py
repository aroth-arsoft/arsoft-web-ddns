#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='arsoft-web-ddns',
		version='1.1',
		description='Simple dynamic DNS service',
		author='Andreas Roth',
		author_email='aroth@arsoft-online.com',
		url='http://www.arsoft-online.com/',
		packages=['arsoft.web.ddns'],
		scripts=['arsoft-ddns'],
		data_files=[
            ('/usr/share/pyshared/arsoft/web/ddns', ['dispatch.fcgi']),
            ('/etc/arsoft/web/ddns', ['config/settings.py']),
            ('/usr/lib/arsoft-web-ddns', ['manage.py']),
            ]
		)
