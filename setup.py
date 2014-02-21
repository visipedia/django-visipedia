#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


INSTALL_REQUIRES = [
	"django >=1.4",
	"requests >=2.0",
]

setup(
	name = "django-visipedia",
	version = "dev",
	description = "The Visipedia login and API for Django.",
	long_description = "",
	keywords = "django, visipedia",
	author = "Jan Jakes, Tomas Matera",
	author_email = "jan@jakes.pro",
	url = "https://github.com/visipedia/django-visipedia",
	license = "MIT",
	packages = ['django_visipedia'],
	package_data = {'': ['LICENSE', 'README.md'], 'django_visipedia': ['*.crt']},
	include_package_data = True,
	install_requires = INSTALL_REQUIRES,
)
