# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Implementations of different file processors."""

from __future__ import absolute_import, print_function
from invenio_files_rest.models import FileInstance
from invenio_grobid.api import process_pdf_stream
from invenio_grobid.mapping import tei_to_dict
from invenio_grobid.errors import GrobidRequestError

def can_process(object_version):
    # For now, we only check the filetype
    return object_version.mimetype == 'application/pdf'

def process(object_version):
    file_instance = FileInstance.get(object_version.file_id)
    with open(file_instance.uri, 'rb') as pdf_file:
        try:
            xml = process_pdf_stream(pdf_file)
        except GrobidRequestError:
            # Question: what is our convention to handle exception?
            # It may be not a good practice to just abort with a code
            abort(500)
    r = tei_to_dict(xml)
    # showing the JSON for debugging
    metadata = dict(
        title=r.get('title'),
        description=r.get('abstract'),
        keywords=[it['value'] for it in r['keywords']] if 'keywords' in r else None,
        creators=[dict(name=it['name'], affiliation=it['affiliations'][0]['value'])
        for it in r['authors']] if 'authors' in r else None
    )
    return metadata
