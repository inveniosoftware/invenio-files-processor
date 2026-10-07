..
    SPDX-FileCopyrightText: 2020 CERN.
    SPDX-License-Identifier: MIT

=========================
 Invenio-Files-Processor
=========================

.. image:: https://github.com/inveniosoftware/invenio-files-processor/workflows/CI/badge.svg
        :target: https://github.com/inveniosoftware/invenio-files-processor/actions

.. image:: https://img.shields.io/coveralls/inveniosoftware/invenio-files-processor.svg
        :target: https://coveralls.io/r/inveniosoftware/invenio-files-processor

.. image:: https://img.shields.io/github/tag/inveniosoftware/invenio-files-processor.svg
        :target: https://github.com/inveniosoftware/invenio-files-processor/releases

.. image:: https://img.shields.io/pypi/dm/invenio-files-processor.svg
        :target: https://pypi.python.org/pypi/invenio-files-processor

.. image:: https://img.shields.io/github/license/inveniosoftware/invenio-files-processor.svg
        :target: https://github.com/inveniosoftware/invenio-files-processor/blob/master/LICENSE

Invenio module for files' processing and or transforming.

It gives a bucket's files a place to be run through something that reads or
rewrites them - extracting text and metadata, converting a format, generating a
preview - without each module having to arrange that for itself.

- A ``FilesProcessor`` interface: a processor says whether it ``can_process`` an
  ``ObjectVersion`` and what to do with it, and the module checks the file is
  readable before handing it over.
- A registry of processors, reachable through the ``current_processors`` proxy.
  Processors register themselves through the ``invenio_files_processor`` entry
  point, or at runtime with ``register_processor``.
- A ``file_processed`` signal, sent with the processor's id, the file and its
  result, so other modules can pick the output up - indexing the extracted text,
  say - without being called by the processor directly.
- One processor included, ``tika_unpack``, which sends a file to an `Apache Tika
  <https://tika.apache.org/>`_ server and returns its text and metadata. Point
  ``FILES_PROCESSOR_TIKA_SERVER_ENDPOINT`` at that server.

Further documentation is available on
https://invenio-files-processor.readthedocs.io/
