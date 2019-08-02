# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""InvenioFilesProcessor configuration."""

FILES_PROCESSOR_PERMISSION_FACTORY = \
    'invenio_files_rest.permissions.permission_factory'
"""Permission factory to control the files access from the files-processor
   interface."""
