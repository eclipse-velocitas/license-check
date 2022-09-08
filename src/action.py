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

"""Github Action which finds and checks all licenses used by a software project."""

import argparse
import sys
from distutils.util import strtobool
from typing import Any

import yaml
from git import Actor, Repo

from licensevalidator.lib.dependency import DependencyInfo
from licensevalidator.lib.utils import print_step
from licensevalidator.licensevalidator import validate_used_licenses
from licensevalidator.noticegenerator import generate_notice_file


def get_args():
    """Obtain all command line arguments given to the script."""
    parser = argparse.ArgumentParser(
        "Finds and checks all licenses of the given software project"
    )
    parser.add_argument(
        "generate_notice_file",
        type=lambda x: bool(strtobool(x)),
        help="Should a notice file be generated?",
    )
    parser.add_argument("notice_file_name", type=str, help="Name of the notice file")
    parser.add_argument(
        "fail_on_violation",
        type=lambda x: bool(strtobool(x)),
        help="Shall the action fail upon license violation?",
    )
    parser.add_argument(
        "config_file_path",
        type=str,
        help="Path to the license check configuration." "(Relative to repository root)",
    )

    return parser.parse_args()


def is_dirty(repo_root_path: str, file_path: str) -> bool:
    """Return true is the specified file is changed ("is dirty"); false otherwise.

    Args:
        repo_root_path (str): The path to the root of the repository.
        file_path (str): The path to the file to check.
    """
    repo = Repo(repo_root_path)
    return repo.is_dirty(path=f"{repo_root_path}/{file_path}")


def output_update_hint(repo_root_path: str, notice_file_name: str) -> None:
    """Output a hint that the notice file needs to be updated manually.

    Args:
        repo_root_path (str): The path to the root of the repository.
        notice_file_name (str): Name of the notice file to check.
    """
    print(f"::warning::{notice_file_name} needs to be updated!")
    print(f"You may copy the updated contents from here:")
    print(f"=========================================================================================================================")
    print(f"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    with open(f"{repo_root_path}/{notice_file_name}", "r") as f:
        print(f.read())
    print(f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(f"=========================================================================================================================")


def read_config_file(config_file_path: str) -> Any:
    """Read the config file located at the provided path.

    Args:
        config_file_path (str): The path to the config file.

    Returns:
        Any: An arbitrary object containing the configuration.
    """
    try:
        with open(config_file_path, "r", encoding="utf-8") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as err:
                print(f"::error::{err}")
    except Exception as file_err:
        print(f"::error::{file_err}")

    return None


def main():
    """Execute the action which executes all steps of the license-validator."""
    args = get_args()

    config = read_config_file(args.config_file_path)

    github_workspace = "/github/workspace"

    licenses_are_valid = False
    origin_to_licenses: dict[str, list[DependencyInfo]] = {}
    try:
        licenses_are_valid, origin_to_licenses = validate_used_licenses(
            github_workspace,
            config["scan-dirs"],
            config["whitelist-file-path"],
        )
    except FileNotFoundError as err:
        print(f"::error::{err}")
        sys.exit(-1)

    if args.generate_notice_file:
        print_step("Generating notice file")
        notice_file_path = f"{args.notice_file_name}.md"
        generate_notice_file(
            origin_to_licenses, f"{github_workspace}/{notice_file_path}"
        )
        if is_dirty(github_workspace, notice_file_path):
            output_update_hint(github_workspace, notice_file_path)
            print("::set-output name=notice-file-is-dirty::true")
        else:
            print("::set-output name=notice-file-is-dirty::false")
        print(f"::set-output name=notice-file-path::{notice_file_path}")

    if not licenses_are_valid and args.fail_on_violation:
        print("::error::License check failed. At least one invalid license found!")
        sys.exit(1)


if __name__ == "__main__":
    main()
