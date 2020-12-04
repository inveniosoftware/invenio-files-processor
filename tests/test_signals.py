# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test file signals."""

from invenio_files_processor.proxies import current_processors
from invenio_files_processor.signals import file_processed
from tests.mock_module.processors import DummyProcessor


def test_signals(dummy_app, object_version):
    """Test file_processed signal."""
    calls = []

    def file_processed_listener(base_app, processor_id, file, data):
        assert processor_id == DummyProcessor.id
        assert object_version == file
        assert data['content'] == 'dummy'

        calls.append('file-processed')

    file_processed.connect(file_processed_listener, weak=False)

    try:
        processor = current_processors.get_processor(name=DummyProcessor.id)

        processor.process(object_version=object_version)

        assert calls == ['file-processed']
    finally:
        file_processed.disconnect(file_processed_listener)
