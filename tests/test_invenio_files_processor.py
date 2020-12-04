# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

import pytest
from flask import Flask
from mock import patch

from invenio_files_processor import InvenioFilesProcessor
from invenio_files_processor.errors import DuplicatedProcessor, \
    InvalidProcessor, UnsupportedProcessor
from invenio_files_processor.processors.processor import FilesProcessor
from invenio_files_processor.processors.tika.unpack import UnpackProcessor
from invenio_files_processor.proxies import current_processors
from tests.mock_module.processors import DummyProcessor


def test_version():
    """Test version import."""
    from invenio_files_processor import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioFilesProcessor(app)
    assert 'invenio-files-processor' in app.extensions

    app = Flask('testapp')
    ext = InvenioFilesProcessor()
    assert 'invenio-files-processor' not in app.extensions
    ext.init_app(app)
    assert 'invenio-files-processor' in app.extensions


def test_load_entry_point_group(processor_entrypoints):
    """Test entry point loading."""
    with patch(
        'invenio_files_processor.ext.iter_entry_points',
        return_value=processor_entrypoints('invenio_files_processor')
    ):
        app = Flask('testapp')
        InvenioFilesProcessor(app)
        app.app_context().push()

        assert set(current_processors.processors.keys()) == {'dummy'}


def test_process(dummy_app, object_version):
    """Test process."""
    processor = current_processors.get_processor(name=DummyProcessor.id)

    test_cases = [
        dict(
            name="Invalid File Case",
            obj="file.pdf",
            exception=FileNotFoundError,
            can_process=True
        ),
        dict(
            name="Invalid Processor Case",
            obj=object_version,
            exception=InvalidProcessor,
            can_process=False
        ),
        dict(
            name="Valid Processor Case",
            obj=object_version,
            exception=None,
            can_process=True
        )
    ]

    for case in test_cases:
        if case['exception'] is None:
            processor.process(case['obj'], can_process=case['can_process'])

            continue

        with pytest.raises(case['exception']):
            processor.process(case['obj'], can_process=case['can_process'])


def test_register_unregister_processor(appctx):
    """Test register and unregister processor flow."""
    current_processors.register_processor(
        DummyProcessor.id,
        DummyProcessor,
    )

    with pytest.raises(DuplicatedProcessor):
        current_processors.register_processor(
            DummyProcessor.id,
            DummyProcessor,
        )

    current_processors.unregister_processor(DummyProcessor.id)

    with pytest.raises(UnsupportedProcessor):
        current_processors.get_processor(DummyProcessor.id)


def test_get_processor(dummy_app):
    """Test register processor."""
    processor = current_processors.get_processor(name=DummyProcessor.id)
    assert isinstance(processor, FilesProcessor)

    with pytest.raises(UnsupportedProcessor):
        processor = current_processors.get_processor(name="invalid")


def test_processors(base_app, object_version):
    """Test process."""
    test_cases = [
        dict(
            name="Unpack Processor",
            processor=UnpackProcessor,
            input=object_version,
            expected="tika.output.json"
        ),
    ]

    for case in test_cases:
        print(case['processor'].id)
        processor = current_processors.get_processor(case['processor'].id)
        output = processor.process(object_version=case['input'])

        assert 'metadata' in output
        assert 'content' in output
