# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Implementations of different file processors."""

from __future__ import absolute_import, print_function

from io import open

from flask import abort, current_app
from invenio_files_rest.models import FileInstance
from invenio_grobid.api import process_pdf_stream
from invenio_grobid.errors import GrobidRequestError
from invenio_grobid.mapping import tei_to_dict


def can_process(object_version):
    """Check if given file can be processed by Grobid."""
    # For now, we only check the filetype
    return object_version.mimetype == 'application/pdf'


def process(object_version):
    """Process the file with Grobid."""
    file_instance = FileInstance.get(object_version.file_id)
    xml = None
    with open(file_instance.uri, 'rb') as pdf_file:
        try:
            xml = process_pdf_stream(pdf_file)
        except GrobidRequestError:
            current_app.logger.warning(
                ('grobid request fails when processing the file {}.'.format(
                    object_version.version_id)),
                exc_info=True
            )
            abort(500)
    r = tei_to_dict(xml)
    # showing the JSON for debugging
    metadata = dict(
        title=r.get('title'),
        description=r.get('abstract'),
        keywords=[it['value']
                  for it in r['keywords']] if 'keywords' in r else None,
        creators=[dict(
            name=it['name'],
            affiliation=it['affiliations'][0]['value']
            if len(it['affiliations']) else None
        ) for it in r['authors']] if 'authors' in r else None
    )
    return metadata
