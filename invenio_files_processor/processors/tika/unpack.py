# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Tika file processor."""
from flask import current_app
from tika import unpack

from ..processor import FilesProcessor

READ_MODE_BINARY = 'rb'


class UnpackProcessor(FilesProcessor):
    """Tika processor."""

    id = 'tika_unpack'

    def can_process(self, object_version, **kwargs):
        """Check if given file can be processed."""
        return object_version.file.readable

    def process_file(self, object_version, **kwargs):
        """Process the file with Tika."""
        fp = object_version.file.storage(**kwargs).open(mode=READ_MODE_BINARY)

        server_url = current_app.config['FILES_PROCESSOR_TIKA_SERVER_ENDPOINT']
        req_opts = current_app.config['FILES_PROCESSOR_TIKA_REQUEST_OPTIONS']

        try:
            result = unpack.from_file(
                fp,
                serverEndpoint=server_url,
                requestOptions=req_opts,
            )
        finally:
            fp.close()

        return result
