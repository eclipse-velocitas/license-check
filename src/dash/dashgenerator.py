# /********************************************************************************
# * Copyright (c) 2023 Contributors to the Eclipse Foundation
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

def generate_dependency(
    path_to_clearlydefined_input: str, origin_to_dependencies: dict[str, list[DependencyInfo]]
) -> None:
    """Generate a notice file from the given dependencies in 
        type/provider/namespace/name/revision format"""
    with open(path_to_clearlydefined_input, "w", encoding="utf-8") as file:
        for origin, dep_infos in origin_to_dependencies.items():
            for dep_info in dep_infos:
                if origin == "Python":
                    file.write(f"pypi/pypi/-/{dep_info.name}/{dep_info.version}\n")
    return
