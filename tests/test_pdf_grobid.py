# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
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

"""pdf_grobid tests."""

from __future__ import absolute_import, print_function

import importlib
import os
from io import open

import pytest
from pkg_resources import EntryPoint

from invenio_files_processor.processors import pdf_grobid


class MockEntryPoint(EntryPoint):
    """Mocking of entrypoint."""

    def load(self):
        """Mock load entry point."""
        return importlib.import_module(self.module_name)


@pytest.fixture()
def tei_xml():
    """Provide pdf fixture."""
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', 'article.xml'), encoding='utf-8') as f:
        yield f.read()


def login_user(client, user):
    """Log in a specified user."""
    with client.session_transaction() as sess:
        sess['user_id'] = user.id if user else None
        sess['_fresh'] = True


def test_permission(mocker, client, users, pdf_obj):
    """Test the file permission."""
    mocker.patch('pkg_resources.iter_entry_points',
                 return_value=[
                     MockEntryPoint(
                         'pdf_grobid',
                         'invenio_files_processor.processors.pdf_grobid')
                 ],
                 auto_spec=True)

    mocker.patch('invenio_files_processor.processors.pdf_grobid.process',
                 return_value={},
                 auto_spec=True)

    login_user(client, users['read'])
    resp = client.post(
        '/filesprocessor/pdf_grobid/{}'.format(pdf_obj.version_id))
    assert resp.status_code == 200

    login_user(client, users['non-read'])
    resp = client.post(
        '/filesprocessor/pdf_grobid/{}'.format(pdf_obj.version_id))
    # see invenio_files_rest.views.check_permission for the description of
    # error codes (401, 403 and 404)
    assert resp.status_code == 404


def test_can_process(pdf_obj, fits_obj):
    """Test the can_process function."""
    assert pdf_grobid.can_process(pdf_obj)
    assert not pdf_grobid.can_process(fits_obj)


def test_process(mocker, pdf_obj, tei_xml):
    """Test the processing function."""
    mocker.patch('invenio_grobid.api.process_pdf_stream',
                 return_value=tei_xml,
                 auto_spec=True)

    metadata = pdf_grobid.process(pdf_obj)
    assert metadata['title'] == "The Need to Fairly Confront Spin-1 for " \
        "the New Higgs-like Particle"
    assert metadata['description'] == (
        "Spin-1 was ruled out early in LHC "
        "reports of a new particle with mass near 125 GeV. Actually the spin-1"
        " possibility was dismissed on false premises, and remains open. "
        "Model-independent classification based on Lorentz invariance permits "
        "nearly two dozen independent amplitudes for spin-1 to two vector "
        "particles, of which two remain with on-shell photons. The Landau-Yang"
        " theorems are inadequate to eliminate spin-1. Theoretical prejudice "
        "to close the gaps is unreliable, and a fair consideration based on "
        "experiment is needed. A spin-1 field can produce the resonance "
        "structure observed in invariant mass distributions, and also produce "
        "the same angular distribution of photons and ZZ decays as spin-0. "
        "However spin-0 cannot produce the variety of distributions made by "
        "spin-1. The Higgs-like pattern of decay also cannot rule out spin-1 "
        "without more analysis. Upcoming data will add information, which "
        "should be analyzed giving spin-1 full and unbiased consideration "
        "that has not appeared before."
    )
    assert metadata['keywords'] is None
    assert metadata['creators'] == [
        {
            'affiliation': 'University of Kansas',
            'name': 'John P. Ralston'
        }
    ]
