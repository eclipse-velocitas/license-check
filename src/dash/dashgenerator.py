# Copyright (c) 2023-2025 Contributors to the Eclipse Foundation
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

"""Methods to generate a notice file from given dependencies."""

from licensevalidator.lib.dependency import DependencyInfo


def generate_dash_input(
    path_to_output_file: str, origin_to_dependencies: dict[str, list[DependencyInfo]]
) -> None:
    """Generate a notice file from the given dependencies in
    type/provider/namespace/name/revision format"""
    with open(path_to_output_file, "w", encoding="utf-8") as file:
        for origin, dep_infos in origin_to_dependencies.items():
            for dep_info in dep_infos:
                try:
                    file.write(
                        f"{get_type_provider_namespace_prefix(origin)}{dep_info.name}/{dep_info.version}\n"
                    )
                except KeyError as err:
                    print(f"Uknown origin {origin}")
                    print(f"Error: {err}")
                    continue


def get_type_provider_namespace_prefix(origin: str) -> str:
    """Map origin to prefix

    Args:
        origin (str): Name of origin

    Returns:
        str: Prefix for ClearlyDefined ID SBOM
    """
    mapping = {
        "Python": "pypi/pypi/-/",
        "Workflows": "git/github/",
        "Rust": "crate/cratesio/-/",
        "Conan": "conan/center/-/",
    }
    return mapping[origin]
