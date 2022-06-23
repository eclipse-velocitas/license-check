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


def commit_notice_file_if_dirty(
    repo_root_path: str, notice_file_name: str, push: bool = True
) -> None:
    """Commit the generated notice file as the given committer.

    Args:
        repo_root_path (str): The path to the root of the repository.
        notice_file_name (str): Name of the notice file to commit.
        push (bool): Should the commit be pushed to the remote.
    """
    repo = Repo(repo_root_path)
    author = Actor("Github Automation", "github-automation@users.noreply.github.com")
    repo.index.add(f"{notice_file_name}.md")

    if repo.is_dirty():
        repo.index.commit(
            f"Update {notice_file_name}.md", author=author, committer=author
        )

        if push:
            origin = repo.remote(name="origin")
            origin.push()


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

    if not licenses_are_valid and args.fail_on_violation:
        print("::error::License check failed. At least one invalid license found!")
        sys.exit(1)

    if args.generate_notice_file:
        print_step("Generating notice file")
        generate_notice_file(
            origin_to_licenses, f"{github_workspace}/{args.notice_file_name}.md"
        )
        commit_notice_file_if_dirty(github_workspace, args.notice_file_name)


if __name__ == "__main__":
    main()
