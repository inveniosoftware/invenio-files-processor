# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""
import os
import tempfile

import pytest
from invenio_app.factory import create_app as create_invenio_app
from invenio_base.utils import entry_points
from invenio_files_rest.models import ObjectVersion

from invenio_files_processor.proxies import current_processors
from tests.mock_module.processors import DummyProcessor


@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    return create_invenio_app


@pytest.fixture()
def dummy_app(appctx):
    """Dummy application fixture."""
    current_processors.register_processor(
        DummyProcessor.id,
        DummyProcessor,
    )

    yield appctx

    current_processors.unregister_processor(DummyProcessor.id)


class MockEntryPoint:
    """Stand-in for an importlib.metadata entry point.

    ``importlib.metadata.EntryPoint`` is immutable, so unlike the
    ``pkg_resources`` one its ``load()`` cannot be reassigned by a fixture.
    """

    def __init__(self, name, group):
        """Initialize the entry point."""
        self.name = name
        self.value = name
        self.group = group

    def load(self):
        """Return the processor factory."""
        return lambda: DummyProcessor


def mock_iter_entry_points_factory(data, mocked_group):
    """Create a mock entry_points function."""
    def entrypoints(group, name=None):
        if group == mocked_group:
            for entrypoint in data:
                yield entrypoint
        else:
            for x in entry_points(group=group):
                yield x

    return entrypoints


@pytest.fixture()
def processor_entrypoints():
    """Entrypoint fixture."""
    eps = [MockEntryPoint(DummyProcessor.id, 'invenio_files_processor')]

    return mock_iter_entry_points_factory(eps, 'invenio_files_processor')


@pytest.fixture()
def bucket(bucket_from_dir):
    """Create temporary bucket fixture."""
    content = b'some content'
    dir_for_files = tempfile.mkdtemp()
    with open(
        os.path.join(dir_for_files, 'output_file'),
        'wb'
    ) as file_out:
        file_out.write(content)

    # load file to bucket
    bucket = bucket_from_dir(dir_for_files)

    yield bucket


@pytest.fixture()
def object_version(database, bucket):
    """Create ObjectVersion fixture."""
    file_from_bucket = ObjectVersion.get_by_bucket(bucket).one()

    yield file_from_bucket
