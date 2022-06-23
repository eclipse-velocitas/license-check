# /********************************************************************************
# * Copyright (c) 2022 Contributors to the Eclipse Foundation
# *
# * See the NOTICE file(s) distributed with this work for additional
# * information regarding copyright ownership.
# *
# * This program and the accompanying materials are made available under the
# * terms of the Apache License 2.0 which is available at
# * http://www.apache.org/licenses/LICENSE-2.0
# *
# * SPDX-License-Identifier: Apache-2.0
# ********************************************************************************/

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
