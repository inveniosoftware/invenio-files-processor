# SPDX-FileCopyrightText: 2020 CERN.
# SPDX-License-Identifier: MIT

"""Proxy for current files processor."""

from flask import current_app
from werkzeug.local import LocalProxy


def _get_current_processors():
    """Return current state of the processors extension."""
    return current_app.extensions['invenio-files-processor']


current_processors = LocalProxy(_get_current_processors)
