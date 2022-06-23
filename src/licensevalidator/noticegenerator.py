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

"""Methods to generate a notice file from given dependencies."""

from licensevalidator.lib.dependency import DependencyInfo


def generate_notice_file(
    origin_to_dependencies: dict[str, list[DependencyInfo]], path_to_notice_file: str
) -> None:
    """Generate a notice file from the given dependencies.

    Args:
        origin_to_dependencies (dict[str, list[DependencyInfo]]):
            Maps the origin (language name or path) to the list of
            dependencies used.
        path_to_notice_file (str):
            The path at which to output the notice file.
    """
    with open(path_to_notice_file, "w", encoding="utf-8") as file:
        file.write("# Licenses Notice\n")
        file.write("*Note*: This file is auto-generated. Do not modify it manually.\n")
        for origin, dep_infos in origin_to_dependencies.items():
            file.write(f"## {origin}\n")
            file.write("| Dependency | Version | License |\n")
            file.write("|:-----------|:-------:|--------:|\n")
            for dep_info in dep_infos:
                licenses_str = "<br/>".join(dep_info.licenses)
                file.write(f"|{dep_info.name}|{dep_info.version}|{licenses_str}|\n")
