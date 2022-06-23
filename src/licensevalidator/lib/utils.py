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

"""Provides utility methods required by various modules."""


def print_step(step_description: str) -> None:
    """Pretty-prints the step description passed to the method to stdout.

    Args:
        step_description (str): A textual description of the step.
    """
    print("##########################################################")
    print(f"### {step_description:<50} ###")
    print("##########################################################")
