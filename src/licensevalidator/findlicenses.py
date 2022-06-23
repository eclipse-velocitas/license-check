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


def find_licenses(
    project_root: str, scan_directories_config: list[Any]
) -> dict[str, list[DependencyInfo]]:
    """Find all licenses used in the software project.

    Args:
        project_root (str):
            The path to the project's root.
        scan_directories_config (list[Any]):
            A list of directories to scan and their respective configurations.

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
        (
            "c++",
            lambda config: __get_cpp_licenses(
                project_root,
                config.get("path"),
                config.get("cpp-conan-included-profile-files"),
            ),
        ),
        (
            "JavaScript",
            lambda config: execute_license_finder(
                os.path.join(project_root, config.get("path")), package_managers=["npm"]
            ),
        ),
    ]

    project_checks = [
        ("Workflows", lambda: get_workflow_dependencies(project_root)),
    ]

    for scan_directory_config in scan_directories_config:
        print_step(f"Scanning '{scan_directory_config['path']}'")
        for language_check in language_checks:
            print(f"Try finding {language_check[0]} package managers:")

            try:
                deps = sorted(
                    language_check[1](scan_directory_config),
                    key=lambda x: x.name.lower(),
                )
                if len(deps) > 0:
                    origin_to_deps[language_check[0]] = deps
            except Exception as err:
                print(f"Found an issue!: {err}")

    for project_check in project_checks:
        print_step(f"Getting dependencies for {project_check[0]}")
        deps = sorted(project_check[1](), key=lambda x: x.name.lower())
        if len(deps) > 0:
            origin_to_deps[project_check[0]] = deps

    return origin_to_deps
