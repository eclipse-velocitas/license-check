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

"""Unit tests for checklicenses."""

import sys

sys.path.append("./src")

from licensevalidator.checklicenses import check_licenses
from licensevalidator.lib.dependency import DependencyInfo


def test_whitelisted_licenses_empty():
    """Test handling of empty whitelist."""
    result = check_licenses(
        "Test",
        [
            DependencyInfo("Dep 1", "Version 1", "License 1"),
            DependencyInfo("Dep 2", "Version 2", "License 2"),
        ],
        [],
    )

    assert result is False


def test_whitelisted_licenses_does_contain_all_licenses():
    """Test handling of only whitelisted licenses."""
    result = check_licenses(
        "Test",
        [
            DependencyInfo("Dep 1", "Version 1", ["License 1"]),
            DependencyInfo("Dep 2", "Version 2", ["License 2"]),
        ],
        ["License 1", "License 2"],
    )

    assert result is True


def test_whitelisted_licenses_does_not_contain_all_licenses():
    """Test handling of non whitelisted licenses."""
    result = check_licenses(
        "Test",
        [
            DependencyInfo("Dep 1", "Version 1", ["License 1"]),
            DependencyInfo("Dep 2", "Version 2", ["License 2"]),
        ],
        ["License 1"],
    )

    assert result is False
