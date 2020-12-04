# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for files' processing and or transforming."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'pytest-invenio>=1.4.0',
    'mock>=3.0.5',
    'invenio-db>=1.0.4',
    'invenio-app>=1.2.3'
]

extras_require = {
    'docs': [
        'Sphinx>=3',
    ],
    # tika processor
    'tika': [
        'tika==1.24',
    ],
    'tests': tests_require,
    'all': [
    ]
}

for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = ["Babel>=2.4.0", "pytest-runner>=3.0.0,<5"]

install_requires = [
    'Flask-BabelEx>=0.9.4',
    'blinker>=1.4',
    'invenio-files-rest>=1.0.6',
    'tika==1.24',
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
    keywords='invenio files processor',
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
        'invenio_base.api_apps': [
            'invenio_files_processor = '
            'invenio_files_processor:InvenioFilesProcessor',
        ],
        'invenio_files_processor': [
            'tika_unpack = '
            'invenio_files_processor.processors.tika.unpack:UnpackProcessor'
        ]
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 3 - Alpha',
    ],
)
