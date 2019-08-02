# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module for file processing tasks."""

from __future__ import absolute_import, print_function

from flask import Blueprint, abort, current_app, jsonify
from invenio_files_rest.models import ObjectVersion
from invenio_files_rest.views import ObjectResource

from .proxies import current_processor

blueprint = Blueprint(
    'invenio_files_processor',
    __name__,
    url_prefix='/filesprocessor',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route("/<processor_name>/<version_id>", methods=['POST'])
def extract_pdf_metadata(processor_name=None, version_id=None):
    """Main file processing endpoint."""
    processor = current_processor.get_processor(processor_name)
    object_version = ObjectVersion.query.filter_by(version_id=version_id).one()

    # this function will check for  'object-read' permission
    ObjectResource.check_object_permission(object_version)

    if processor.can_process(object_version):
        try:
            metadata = processor.process(object_version)
            return jsonify(metadata)
        except Exception:
            current_app.logger.warning(
                ('The processor {} fails when processing the file {}.'.format(
                    processor_name, version_id)),
                exc_info=True
            )
            abort(500)
    else:
        current_app.logger.warning(
            ('The processor {} cannot process the file {}.'.format(
                processor_name, version_id)), exc_info=True
        )
        abort(500)
