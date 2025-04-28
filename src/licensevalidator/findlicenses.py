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

"""Methods and classes to find all licenses of a software project."""

import os
import shutil
from typing import Any, Optional

from licensevalidator.lib.dependency import DependencyInfo
from licensevalidator.lib.licensefinder import execute_license_finder
from licensevalidator.lib.utils import print_step
from licensevalidator.lib.workflowlicenses import get_workflow_dependencies


def __get_python_licenses(
    project_root: str,
    scan_dir: str,
    python_version: int,
    included_requirement_files: list[str],
) -> set[DependencyInfo]:
    dependencies: set[DependencyInfo] = set()

    if included_requirement_files is not None:
        for requirement_file in included_requirement_files:
            dependencies.update(
                execute_license_finder(
                    os.path.join(project_root, scan_dir),
                    pip_requirements_path=requirement_file,
                    python_version=python_version,
                    package_managers=["pip"],
                )
            )
    else:
        dependencies.update(
            execute_license_finder(
                os.path.join(project_root, scan_dir),
                python_version=python_version,
                package_managers=["pip"],
            )
        )

    return dependencies


def __get_cpp_licenses(
    project_root: str, scan_dir: str, conan_profile_files: Optional[list[str]]
) -> set[DependencyInfo]:
    dependencies: set[DependencyInfo] = set()

    if conan_profile_files is not None:
        for conan_profile_file in conan_profile_files:
            __use_conan_profile_if_present(
                os.path.join(project_root, scan_dir, conan_profile_file)
            )
            dependencies.update(
                execute_license_finder(
                    os.path.join(project_root, scan_dir), package_managers=["conan"]
                )
            )
        return dependencies
    else:
        dependencies.update(
            execute_license_finder(
                os.path.join(project_root, scan_dir), package_managers=["conan"]
            )
        )

    return dependencies


def __use_conan_profile_if_present(conan_profile_file: str):
    """Replace the file containing the conan default profile by a copy of the
    passed conan_profile_file.
    This is a workaround since the pivotal LicenseFinder is internally
    using this default profile when calling conan install.

    Args:
        conan_profile_file (str):
            File defining the profile used by Conan (relative to project_root).
    """
    if conan_profile_file:
        if not os.path.isfile(conan_profile_file):
            raise FileNotFoundError(
                f'Conan profile file "{conan_profile_file}" does not exist!'
            )

        conan_home_dir = os.environ.get("CONAN_USER_HOME")
        if not conan_home_dir:
            conan_home_dir = os.environ.get("HOME")
        if not conan_home_dir:
            conan_home_dir = "/root"
        conan_default_profile_file = os.path.join(
            conan_home_dir, ".conan/profiles/default"
        )

        os.makedirs(os.path.dirname(conan_default_profile_file), exist_ok=True)
        shutil.copyfile(conan_profile_file, conan_default_profile_file)
        if not os.path.isfile(conan_default_profile_file):
            raise FileNotFoundError(
                f'Failed to use Conan profile file "{conan_profile_file}"!'
            )

        conan2_home_dir = os.environ.get("CONAN_HOME")
        if not conan2_home_dir:
            conan2_home_dir = os.environ.get("HOME")
            if not conan2_home_dir:
                conan2_home_dir = "/root"
            os.path.join(conan2_home_dir, ".conan2")
        conan2_default_profile_file = os.path.join(
            conan2_home_dir, "profiles", "default"
        )

        os.makedirs(os.path.dirname(conan2_default_profile_file), exist_ok=True)
        shutil.copyfile(conan_profile_file, conan2_default_profile_file)
        if not os.path.isfile(conan2_default_profile_file):
            raise FileNotFoundError(
                f'Failed to use Conan2 profile file "{conan_profile_file}"!'
            )


def sort_dependencies(deps: list[DependencyInfo]) -> list[DependencyInfo]:
    """Sort the passed DependencyInfo list by name 1st and version 2nd

    Args: deps (list[DependencyInfo]):
        The list of dependencies to be sorted

    Returns:
        A new list with sorted contents
    """
    deps = sorted(deps, key=lambda x: x.version.lower())
    deps = sorted(deps, key=lambda x: x.name.lower())
    return deps


def find_licenses(
    project_root: str,
    scan_directories_config: list[Any],
    github_token: str = None,
) -> dict[str, list[DependencyInfo]]:
    """Find all licenses used in the software project.

    Args:
        project_root (str):
            The path to the project's root.
        scan_directories_config (list[Any]):
            A list of directories to scan and their respective configurations.
        github-token (str):
            GitHub token to do authorized API requests (overcoming rate limiting)

    Returns:
        dict[str,list[DependencyInfo]]: Dict containing mappings from
            origin -> list of dependencies. Where origin can be
            Python, Github Workflows or other programming/markup languages.
    """

    origin_to_deps: dict[str, list[DependencyInfo]] = {}

    language_checks = [
        (
            "Python",
            lambda config: __get_python_licenses(
                project_root,
                config.get("path"),
                config.get("python-version", 3),
                config.get("python-pip-included-requirement-files"),
            ),
        ),
        (
            "Rust",
            lambda config: execute_license_finder(
                os.path.join(project_root, config.get("path")),
                package_managers=["cargo"],
            ),
        ),
        # Disable Conan scan - not working yet - enable once fixed
        # GitHub issue: https://github.com/pivotal/LicenseFinder/issues/1057
        # (
        #     "c++",
        #     lambda config: __get_cpp_licenses(
        #         project_root,
        #         config.get("path"),
        #         config.get("cpp-conan-included-profile-files"),
        #     ),
        # ),
        (
            "JavaScript",
            lambda config: execute_license_finder(
                os.path.join(project_root, config.get("path")), package_managers=["npm"]
            ),
        ),
    ]

    project_checks = [
        ("Workflows", lambda: get_workflow_dependencies(project_root, github_token)),
    ]

    for scan_directory_config in scan_directories_config:
        print_step(f"Scanning '{scan_directory_config['path']}'")
        for language_check in language_checks:
            print(f"Try finding {language_check[0]} package managers:")

            try:
                deps = sort_dependencies(language_check[1](scan_directory_config))
                if len(deps) > 0:
                    origin_to_deps[language_check[0]] = deps
            except Exception as err:
                print(f"Found an issue!: {err}")

    for project_check in project_checks:
        print_step(f"Getting dependencies for {project_check[0]}")
        deps = sort_dependencies(project_check[1]())
        if len(deps) > 0:
            origin_to_deps[project_check[0]] = deps

    return origin_to_deps
