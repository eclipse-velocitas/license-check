# Copyright (c) 2022-2025 Contributors to the Eclipse Foundation
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

"""Unit tests for licensefinder."""

from licensevalidator.lib.licensefinder import execute_license_finder


def test_execution_python():
    """Tests the execution of license finder for python."""
    result = execute_license_finder(
        "./testbench/python-without-workflows/src",
        python_version=3,
        pip_requirements_path="requirements.txt",
    )

    # Two explicit plus two implicit
    assert len(result) == 4

    # List in alphabetical order
    # idna required by yarl
    assert result[0].name == "idna"
    assert result[0].version == "3.7"
    assert result[0].licenses == ["BSD"]

    # multidict required by yarl
    assert result[1].name == "multidict"
    assert result[1].version == "6.0.5"
    assert result[1].licenses == ["Apache 2.0"]

    assert result[2].name == "six"
    assert result[2].version == "1.16.0"
    assert result[2].licenses == ["MIT"]

    assert result[3].name == "yarl"
    assert result[3].version == "1.9.4"
    assert result[3].licenses == ["Apache 2.0"]
