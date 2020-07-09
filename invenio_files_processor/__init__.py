# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for files' processing and or transforming."""

from .ext import InvenioFilesProcessor
from .version import __version__

__all__ = ('__version__', 'InvenioFilesProcessor')
