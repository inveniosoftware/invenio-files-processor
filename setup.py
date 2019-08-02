# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module for file processing tasks."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'Flask-Menu>=0.4.0',
    'check-manifest>=0.25',
    'coverage>=4.0',
    'invenio-db[versioning]>=1.0.0b3',
    'isort>=4.2.15',
    'pydocstyle>=1.0.0',
    'pytest>=2.8.0',
    'pytest-cov>=1.8.0',
    'pytest-mock>=1.6.0',
    'pytest-pep8>=1.0.6',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'invenio-files-rest>=1.0.0a17',
    'invenio-access>=1.0.0a12',
    'invenio-grobid>=0.2.0'
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_files_processor', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-files-processor',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio files processor REST grobid',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-files-processor',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_files_processor = '
            'invenio_files_processor:InvenioFilesProcessor',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_files_processor',
        ],
        'invenio_files_processor.processors': [
            'pdf_grobid = invenio_files_processor.processors.pdf_grobid'
        ]
        # 'invenio_base.api_apps': [],
        # 'invenio_base.api_blueprints': [],
        # 'invenio_base.blueprints': [],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
    ],
)
