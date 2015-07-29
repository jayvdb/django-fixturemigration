# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = 'django-fixturemigration',
    packages = find_packages(),
    version = '0.7',
    description = 'An app to load fixtures inside a migration data step',
    author = 'Emilio A. Sánchez',
    author_email = 'emilio@commite.co',
    url = 'https://github.com/emiliosanchez/django-fixturemigration',
    keywords = ['django', 'migrations', 'fixtures'],
    include_package_data=True,
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
