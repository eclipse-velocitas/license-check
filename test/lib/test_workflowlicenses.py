# Copyright (c) 2022-2023 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for workflowlicenses."""

import sys
from io import StringIO

import pytest

sys.path.append("./src")

from licensevalidator.lib.workflowlicenses import (
    _extract_action_info,
    _get_all_workflow_file_paths,
    _read_used_actions_from_yaml,
)


def test_extract_action_info_with_relative_path():
    """Test valid extraction of info with a relative path."""
    action_info = _extract_action_info("github/codeql-action/init@v2")

    assert action_info.repository == "github/codeql-action"
    assert action_info.relative_path == "init"
    assert action_info.version == "v2"


def test_extract_action_info_without_relative_path():
    """Test valid extraction of info without a relative path."""
    action_info = _extract_action_info("github/codeql-action@v2")

    assert action_info.repository == "github/codeql-action"
    assert action_info.relative_path is None
    assert action_info.version == "v2"


def test_extract_action_info_without_version():
    """Test extraction of info without a version."""
    with pytest.raises(ValueError):
        _extract_action_info("github/codeql-action")


def test_read_actions_from_yml():
    """Test reading actions from yaml."""
    yaml = """name: My workflow

on:
  pull_request:
    branches:
      - main

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    name: Run unit tests and linters

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
        with:
          ref: ${{ github.head_ref }}
    """

    tio = StringIO(yaml)
    dependencies = _read_used_actions_from_yaml(tio)

    assert len(dependencies) == 1
    dep = dependencies.pop()
    assert dep.name == "actions/checkout"
    assert dep.version == "v2"


def test_read_multiple_equal_actions_from_yml():
    """Test reading multiple equal actions from yaml."""
    yaml = """name: My workflow

on:
  pull_request:
    branches:
      - main

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    name: Run unit tests and linters

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2
      with:
        ref: ${{ github.head_ref }}
    - name: Checkout another repository
      uses: actions/checkout@v2
      with:
        ref: ${{ github.head_ref }}
    """

    tio = StringIO(yaml)
    dependencies = _read_used_actions_from_yaml(tio)

    assert len(dependencies) == 1
    dep = dependencies.pop()
    assert dep.name == "actions/checkout"
    assert dep.version == "v2"


def test_find_all_workflow_file_paths():
    """Test the returned workflow file paths."""
    file_paths = _get_all_workflow_file_paths("./testbench/python-with-workflows")

    assert len(file_paths) == 2
    assert (
        file_paths[0] == "./testbench/python-with-workflows/.github/workflows/"
        "my-other-workflow.yaml"
    )
    assert (
        file_paths[1] == "./testbench/python-with-workflows/.github/workflows/"
        "my-workflow.yml"
    )
