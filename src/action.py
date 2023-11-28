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

"""Github Action which finds and checks all licenses used by a software project."""

import argparse
import sys
from typing import Any

import yaml
from git import Repo
from str2bool import str2bool

from dash.dashgenerator import generate_dash_input
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
        type=lambda x: bool(str2bool(x)),
        help="Should a notice file be generated?",
    )
    parser.add_argument("notice_file_name", type=str, help="Name of the notice file")
    parser.add_argument(
        "fail_on_violation",
        type=lambda x: bool(str2bool(x)),
        help="Shall the action fail upon license violation?",
    )
    parser.add_argument(
        "config_file_path",
        type=str,
        help="Path to the license check configuration." "(Relative to repository root)",
    )
    parser.add_argument(
        "--github-token",
        type=str,
        help="Pass GitHub token to overcome possible rate limiting issues",
    )

    parser.add_argument(
        "generate_dash",
        type=lambda x: bool(str2bool(x)),
        help="Generate Eclipse Dash compliant input file",
    )

    return parser.parse_args()


def is_dirty(repo_root_path: str, file_path: str) -> bool:
    """Return true is the specified file is changed ("is dirty"); false otherwise.

    Args:
        repo_root_path (str): The path to the root of the repository.
        file_path (str): The path to the file to check.
    """
    repo = Repo(repo_root_path)
    repo.config_writer("global").set_value(
        "safe", "directory", repo_root_path
    ).release()
    return repo.is_dirty(path=f"{repo_root_path}/{file_path}")


def output_update_hint(repo_root_path: str, notice_file_name: str) -> None:
    """Output a hint that the notice file needs to be updated manually.

    Args:
        repo_root_path (str): The path to the root of the repository.
        notice_file_name (str): Name of the notice file to check.
    """
    print(
        f'::error::{notice_file_name} needs to be manually updated ("checked-in")! '
        "You can copy the updated contents from the workflow output."
    )
    print(
        "============================================================================================================="
    )
    print(
        "Copy from below here (!! Make sure to also copy the newline at the end-of-file !!) ..."
    )
    print(
        "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
    )
    with open(f"{repo_root_path}/{notice_file_name}", "r", encoding="utf8") as file:
        print(file.read())
    print(
        "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    print(
        "... until above here. (!! Make sure to also copy the newline at the end-of-file !!)"
    )
    print(
        "============================================================================================================="
    )


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
            github_token=args.github_token,
        )
    except FileNotFoundError as err:
        print(f"::error::{err}")
        sys.exit(-1)

    workflow_failure = False

    if not licenses_are_valid and args.fail_on_violation:
        print("::error::License check failed. At least one invalid license found!")
        workflow_failure = True

    if args.generate_notice_file:
        print_step("Generating notice file")
        notice_file_path = f"{args.notice_file_name}.md"
        generate_notice_file(
            origin_to_licenses, f"{github_workspace}/{notice_file_path}"
        )
        notice_file_is_dirty = is_dirty(github_workspace, notice_file_path)
        if notice_file_is_dirty:
            output_update_hint(github_workspace, notice_file_path)
            workflow_failure = True

    if args.generate_dash:
        print("Generating Eclipse Dash compliant input file")
        generate_dash_input(
            f"{github_workspace}/clearlydefined.input", origin_to_licenses
        )

    if workflow_failure:
        sys.exit(1)


if __name__ == "__main__":
    main()
