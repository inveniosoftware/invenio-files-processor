# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Signals for Invenio-Files-Processor."""

from blinker import Namespace

_signals = Namespace()

file_processed = _signals.signal('file-processed')
"""File processed signal.

When implementing the event listener, the result can be retrieved from `data`.
Example event listener (subscriber) implementation:
.. code-block:: python
    def listener(sender, processor_id, file, data):
        \"""File processor listener.

        :param sender: current_app.
        :param processor_id: str processor id.
        :param file: ObjectVersion input.
        :param data: Data array with keys metadata and content.
        \"""
        # do something with the data

    from invenio_files_processor.signals import file_processed
    file_processed.connect(listener)
"""
