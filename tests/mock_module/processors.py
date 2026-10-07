# SPDX-FileCopyrightText: 2020 CERN.
# SPDX-License-Identifier: MIT

"""Dummy processor."""

from invenio_files_processor.processors.processor import FilesProcessor


class DummyProcessor(FilesProcessor):
    """Dummy processor."""

    id = "dummy"

    def can_process(self, object_version, **kwargs):
        """Check if given file can be processed."""
        return kwargs.get("can_process", True)

    def process_file(self, object_version, **kwargs):
        """Process the file with Dummy."""
        return dict(content="dummy")
