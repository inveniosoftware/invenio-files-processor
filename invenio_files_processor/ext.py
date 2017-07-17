# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Invenio module that adds more fun to the platform."""

from __future__ import absolute_import, print_function


import pkg_resources
import six
from flask import current_app
from pkg_resources import DistributionNotFound, get_distribution
from werkzeug.utils import cached_property, import_string


from . import config
from .views import blueprint

def obj_or_import_string(value, default=None):
    """Import string or return object."""
    if isinstance(value, six.string_types):
        return import_string(value)
    elif value:
        return value
    return default

def load_or_import_from_config(key, app=None, default=None):
    """Load or import value from config."""
    app = app or current_app
    imp = app.config.get(key)
    return obj_or_import_string(imp, default=default)


class _InvenioFilesProcessorState(object):
    """State object."""

    def __init__(self, app, entry_point_group=None):
        """Initialize state."""
        self.app = app
        self.entry_point_group = entry_point_group
        self.processors = {}

    @cached_property
    def permission_factory(self):
        """Load default permission factory for Buckets collections."""
        return load_or_import_from_config(
            'FILES_PROCESSOR_PERMISSION_FACTORY', app=self.app
        )

    def register_processor(self, name, processor):
        """Register a processor in the system."""
        if name in self.processors:
            assert name not in self.processors, \
                "File processor with same name already registered"
        self.processors[name] = processor

    def load_entry_point_group(self, entry_point_group):
        """Load processors from an entry point group."""
        for ep in pkg_resources.iter_entry_points(group=entry_point_group):
            self.register_processor(ep.name, ep.load())

    def get_processor(self, processor_name=None):
        """Get processors."""
        if self.entry_point_group is not None:
            self.load_entry_point_group(self.entry_point_group)
            self.entry_point_group = None
        return  self.processors[processor_name]

class InvenioFilesProcessor(object):
    """Invenio-Files-Processor extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app, entry_point_group='invenio_files_processor.processors'):
        """Flask application initialization."""
        self.init_config(app)
        app.register_blueprint(blueprint)
        state = _InvenioFilesProcessorState(app, entry_point_group=entry_point_group)
        app.extensions['invenio-files-processor'] = state
        return state

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        if 'BASE_TEMPLATE' in app.config:
            app.config.setdefault(
                'FILES_PROCESSOR_BASE_TEMPLATE',
                app.config['BASE_TEMPLATE'],
            )
        for k in dir(config):
            if k.startswith('FILES_PROCESSOR_'):
                app.config.setdefault(k, getattr(config, k))
