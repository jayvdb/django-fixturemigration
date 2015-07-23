# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name = 'django-fixturemigration',
    packages = ['fixturemigration'],
    version = '0.3',
    description = 'An app to load fixtures inside a migration data step',
    author = 'Emilio A. Sánchez',
    author_email = 'emilio@commite.co',
    url = 'https://github.com/emiliosanchez/django-fixturemigration',
    keywords = ['django', 'migrations', 'fixtures'],
    classifiers = [
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Environment :: Web Environment",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Framework :: Django",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 1.8"
    ],
)
