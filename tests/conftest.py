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

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile
from io import BytesIO, open

import pytest
from flask import Flask
from flask_babelex import Babel
from flask_menu import Menu
from invenio_access import InvenioAccess
from invenio_access.models import ActionUsers
from invenio_accounts import InvenioAccounts
from invenio_accounts.testutils import create_test_user
from invenio_db import db as db_
from invenio_db import InvenioDB
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Bucket, Location, ObjectVersion
from invenio_files_rest.permissions import object_read_all
from sqlalchemy_utils.functions import create_database, database_exists, \
    drop_database

from invenio_files_processor import InvenioFilesProcessor


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path


@pytest.yield_fixture(scope='session', autouse=True)
def app():
    """Flask application fixture."""
    instance_path = tempfile.mkdtemp()

    app_ = Flask('testapp', instance_path=instance_path)
    app_.config.update(
        SECRET_KEY='SECRET_KEY',
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///')
    )
    Babel(app_)
    InvenioDB(app_)
    Menu(app_)
    InvenioAccounts(app_)
    InvenioAccess(app_)
    InvenioFilesREST(app_)
    InvenioFilesProcessor(app_)
    with app_.app_context():
        yield app_
    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def client(app):
    """Get test client."""
    with app.test_client() as client:
        yield client


@pytest.yield_fixture()
def db(app):
    """Setup database."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    db_.create_all()
    yield db_
    db_.session.remove()
    db_.drop_all()
    drop_database(str(db_.engine.url))


@pytest.yield_fixture()
def dummy_location(db):
    """File system location."""
    tmppath = tempfile.mkdtemp()

    loc = Location(
        name='testloc',
        uri=tmppath,
        default=True
    )
    db.session.add(loc)
    db.session.commit()

    yield loc

    shutil.rmtree(tmppath)


@pytest.fixture()
def bucket(db, dummy_location):
    """File system location."""
    b = Bucket.create(location=dummy_location)
    db.session.commit()
    return b


@pytest.fixture()
def pdf_obj(db, bucket):
    """Mock of a PDF document."""
    content = b'pdf content'
    obj = ObjectVersion.create(bucket, 'file.pdf', stream=BytesIO(content),
                               size=len(content))
    db.session.commit()
    return obj


@pytest.fixture()
def tei_xml():
    """Provide pdf fixture."""
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', 'article.xml'), encoding='utf-8') as f:
        return f.read()


@pytest.fixture()
def fits_obj(db, bucket):
    """Mock of a FITS image."""
    content = b'fits content'
    obj = ObjectVersion.create(bucket, 'file.fits', stream=BytesIO(content),
                               size=len(content))
    db.session.commit()
    return obj


@pytest.yield_fixture()
def users(db, bucket):
    """Permission for users."""
    users = {u: create_test_user(
        email='{}@invenio-software.org'.format(u),
        password='password',
        active=True) for u in ['read', 'non-read']}

    db.session.add(ActionUsers(
        action=object_read_all.value,
        argument=str(bucket.id),
        user=users['read']))

    db.session.commit()

    yield users
