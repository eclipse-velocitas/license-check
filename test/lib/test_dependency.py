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

"""Unit tests for dependency."""

import sys

import pytest

sys.path.append("./src")

from licensevalidator.lib.dependency import DependencyInfo


def test_equality():
    """Test the quality of 2 dependencies."""
    dep1 = DependencyInfo("Dep 1", "Version 1", ["License 1"])
    dep2 = DependencyInfo("Dep 1", "Version 1", ["License 1"])

    assert dep1 == dep2


@pytest.mark.parametrize(
    "test_input",
    [
        DependencyInfo("Dep 2", "Version 1", ["License 1"]),
        DependencyInfo("Dep 1", "Version 2", ["License 1"]),
        DependencyInfo("Dep 1", "Version 1", []),
        DependencyInfo("Dep 3", "Version 3", ["A", "B", "C"]),
    ],
)
def test_inequality(test_input: DependencyInfo):
    """Test the inquality of 2 dependencies if name differs."""
    dep = DependencyInfo("Dep 1", "Version 1", ["License 1"])

    assert dep != test_input
