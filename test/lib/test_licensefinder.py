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

"""Unit tests for licensefinder."""

import sys

sys.path.append("./src")

from licensevalidator.lib.licensefinder import execute_license_finder


def test_execution_python():
    """Tests the execution of license finder for python."""
    result = execute_license_finder(
        "./testbench/python-without-workflows/src",
        python_version=3,
        pip_requirements_path="requirements.txt",
    )

    assert len(result) == 2
    assert result[0].name == "grpcio"
    assert result[0].version == "1.44.0"
    assert result[0].licenses == ["Apache 2.0"]
    assert result[1].name == "six"
    assert result[1].version == "1.16.0"
    assert result[1].licenses == ["MIT"]
