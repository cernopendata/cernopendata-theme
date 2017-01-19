# -*- coding: utf-8 -*-
#
# This file is part of CERN Open Data Portal.
# Copyright (C) 2017 CERN.
#
# CERN Open Data Portal is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Open Data Portal is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Open Data Portal; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Module tests."""

from __future__ import absolute_import, print_function

import os
import subprocess

from click.testing import CliRunner
from flask_assets import assets

from invenio_assets.cli import collect, npm


def test_version():
    """Test version import."""
    from cernopendata_theme import __version__
    assert __version__


def test_view(app, script_info):
    """Test assets command in assets CLI."""
    static_root = app.extensions['collect'].static_root
    runner = CliRunner()

    # Generate package.json.
    result = runner.invoke(npm, obj=script_info)
    assert result.exit_code == 0

    filepath = os.path.join(app.static_folder, 'package.json')
    assert os.path.exists(filepath)

    current_dir = os.getcwd()
    os.chdir(app.static_folder)
    exit_status = subprocess.call('npm install', shell=True)
    assert exit_status == 0
    os.chdir(current_dir)

    # Run collect
    result = runner.invoke(collect, ['-v'], obj=script_info)
    assert result.exit_code == 0

    # Run build
    result = runner.invoke(assets, ['build'], obj=script_info)
    assert result.exit_code == 0

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
