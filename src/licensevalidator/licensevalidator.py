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

"""Entry point for the license validator."""

import os
from typing import Any

from licensevalidator.checklicenses import check_licenses, read_license_list
from licensevalidator.findlicenses import find_licenses
from licensevalidator.lib.dependency import DependencyInfo
from licensevalidator.lib.utils import print_step


def validate_used_licenses(
    project_root: str,
    scan_directories_config: list[Any],
    whitelist_file_path: str,
    github_token: str,
) -> tuple[bool, dict[str, list[DependencyInfo]]]:
    """Run the license validation.

    Args:
        project_root (str):
            The path to the project root.
        scan_directories_config (list[Any]):
            A list of directories to scan and their respective configurations.
        whitelist_file_path (str):
            The path to the whitelist file
            (relative to project root).
        github-token (str):
            GitHub token to do authorized API requests (overcoming rate limiting)

    Raises:
        FileNotFoundError: In case the whitelist file is not present.

    Returns:
         tuple[bool, dict[str, list[DependencyInfo]]]:
            A tuple consisting of a pair of
            - True if all used licenses are whitelisted, False otherwise.
            - Dict containing mappings from
              origin -> list of dependencies. Where origin can be
              Python, Github Workflows or other programming/markup languages.
    """
    abs_path_to_whitelist = os.path.join(project_root, whitelist_file_path)
    if not os.path.isfile(abs_path_to_whitelist):
        raise FileNotFoundError(
            f'Whitelist file "{abs_path_to_whitelist}" does not exist!'
        )

    print_step("Finding licenses")
    origin_vs_deps = find_licenses(project_root, scan_directories_config, github_token)

    print_step("Checking licenses")
    whitelisted_licenses = read_license_list(abs_path_to_whitelist)

    result = True
    for origin, dependencies in origin_vs_deps.items():
        result = check_licenses(origin, dependencies, whitelisted_licenses) and result

    return (
        result,
        origin_vs_deps,
    )
