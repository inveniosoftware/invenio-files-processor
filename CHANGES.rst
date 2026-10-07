..
    SPDX-FileCopyrightText: 2020-2026 CERN.
    SPDX-License-Identifier: MIT

Changes
=======

Version 1.0.0 (released TBD)

- Drop ``pkg_resources``. Processors are loaded through
  ``invenio_base.utils.entry_points``, so the package imports on setuptools 81
  and later, where ``pkg_resources`` is deprecated and removed respectively.
- Add ``invenio-base>=2.3.0`` as a dependency; 2.3.0 is the first release
  providing ``utils.entry_points``.
- Move packaging from ``setup.py`` to ``pyproject.toml`` using hatchling.
  ``setup.cfg``, ``MANIFEST.in`` and ``pytest.ini`` are removed, their settings
  folded into ``pyproject.toml``.
- Require ``invenio-files-rest>=6.0.0``.
- Remove the ``Flask-BabelEx`` dependency. It was declared but never imported,
  and the package ships no translation catalogs. ``babel.ini`` is removed with it.
- Raise ``requires-python`` to 3.10, and widen the ``tika`` extra from a pin
  on ``1.24`` to ``>=3.1.0,<4.0.0``.

Version 0.1.0 (Dec 4, 2020)

- Initial public release.
