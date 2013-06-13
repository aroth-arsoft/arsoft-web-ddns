#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='arsoft-web-ddns',
		version='1.0',
		description='Simple dynamic DNS service',
		author='Andreas Roth',
		author_email='aroth@arsoft-online.com',
		url='http://www.arsoft-online.com/',
		packages=['arsoft.web.ddns'],
		scripts=[],
		data_files=[
            ('/usr/share/pyshared/arsoft/web/ddns', ['dispatch.fcgi']),
            ('/etc/arsoft/web/ddns/static', ['arsoft/web/ddns/static/main.css']),
            ('/etc/arsoft/web/ddns/templates', ['arsoft/web/ddns/templates/home.html']),
            ]
		)
