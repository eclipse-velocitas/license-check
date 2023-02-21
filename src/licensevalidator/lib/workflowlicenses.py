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

"""Methods to read licenses from github workflows."""

import os
import re
from typing import Dict, Optional, TextIO

import requests
import yaml
from yaml.loader import SafeLoader

from licensevalidator.lib.dependency import DependencyInfo


class _ActionInfo:
    """Bundles all infos for a single Github action."""

    def __init__(self, repository: str, relative_path: Optional[str], version: str):
        """Create a new instance.

        Args:
            repository (str): Repository name.
            relative_path (Optional[str]): Relative path within the repo.
            version (str): Version of the action.
        """
        self.repository = repository
        self.relative_path = relative_path
        self.version = version


def _extract_action_info(action_usage_string: str) -> _ActionInfo:
    """Extract all information about an action from its usage string.

    Args:
        action_usage_string (str): The github action usage string.

    Returns:
        _ActionInfo: Extract info from the action.
    """
    needle_index = action_usage_string.index("@")
    action_path = action_usage_string[:needle_index]
    version = action_usage_string[needle_index + 1 :]

    # the action path is formed like this:
    # github_org/repository_name/directory_in_repository/nested_directory_in_repository
    path_pieces = action_path.split("/")
    repository = "/".join(path_pieces[0:2])

    relative_path = None
    if len(path_pieces) > 2:
        relative_path = "/".join(path_pieces[2:])

    return _ActionInfo(repository, relative_path, version)


def _read_used_actions_from_yaml(text_io: TextIO) -> set[DependencyInfo]:
    """Read all used actions from a workflow YAML file.

    Args:
        text_io (TextIO): The io object from which to parse the YAML.

    Returns:
        set[DependencyInfo]: Set containing all used github actions.
    """
    used_actions: set[DependencyInfo] = set()
    data = yaml.load(text_io, Loader=SafeLoader)
    if "jobs" in data:
        jobs: Dict = data["jobs"]

        for _, job_settings in jobs.items():
            if "steps" not in job_settings:
                continue

            steps = job_settings["steps"]
            for step in steps:
                if "uses" not in step:
                    continue

                used_action: str = step["uses"]
                if used_action.find("@") != -1:
                    action_info = _extract_action_info(used_action)

                    used_actions.add(
                        DependencyInfo(action_info.repository, action_info.version, [])
                    )
    else:
        print(f"::warning::Ignoring malformed workflow '{text_io.name}' - missing 'jobs' section")

    return used_actions


def _get_all_workflow_file_paths(project_root: str) -> list[str]:
    """Get the file paths to each workflow file in the github workflow directory.

    Args:
        project_root (str): The path to the project root.

    Returns:
        list[str]: A list of absolute paths to each workflow file.
    """
    workflow_dir = f"{project_root}/.github/workflows"

    if not os.path.isdir(workflow_dir):
        print("No workflows available!")

    workflow_files: list[str] = []
    for workflow_file in os.listdir(workflow_dir):
        if not re.match(r"^.*\.(yml|yaml)$", workflow_file):
            continue

        workflow_files.append(os.path.join(workflow_dir, workflow_file))

    return workflow_files


def _get_used_actions(project_root: str) -> set[DependencyInfo]:
    """Get all used actions from all github workflows.

    Args:
        project_root (str): The path to the project root.

    Returns:
        set[DependencyInfo]: Set of unique actions all github workflows depend on.
    """
    workflow_dir = f"{project_root}/.github/workflows"

    if not os.path.isdir(workflow_dir):
        print("No workflows available!")
        return set()

    used_actions: set[DependencyInfo] = set()
    for workflow_file_path in _get_all_workflow_file_paths(project_root):
        with open(workflow_file_path, encoding="utf-8") as file:
            used_actions.update(_read_used_actions_from_yaml(file))

    return used_actions


def __get_license_for_action(action_repo: str, github_token: str) -> Optional[str]:
    """Get the license for a single github action.

    Args:
        action_repo (str): The action repository name
        github-token (str):
            GitHub token to do authorized API requests (overcoming rate limiting)

    Returns:
        str: The name of the license, if available.
    """
    request_headers={"Accept": "application/vnd.github.v3+json"}
    if github_token is not None:
        request_headers["authorization"] = github_token

    result = requests.get(
        f"https://api.github.com/repos/{action_repo}",
        headers=request_headers,
    )
    try:
        return result.json()["license"]["name"]
    except (KeyError, ValueError) as err:
        print("Error getting workflow license info from github.com:")
        print(f"\t{err}")
        print(f"\t{action_repo}")
        print(f"\t{result.json()}")

    return None


def get_workflow_dependencies(project_root: str, github_token: str) -> list[DependencyInfo]:
    """Get all dependencies used by all workflows.

    Args:
        project_root (str): The project root in which to search for workflows.
        github-token (str):
            GitHub token to do authorized API requests (overcoming rate limiting)

    Returns:
        list[DependencyInfo]: A list of all unique dependencies.
    """
    result: list[DependencyInfo] = []
    for dep_infos in _get_used_actions(project_root):
        license_name = __get_license_for_action(dep_infos.name, github_token)
        if license_name is not None:
            dep_infos.licenses = [license_name]
        result.append(dep_infos)
    return result


if __name__ == "__main__":
    print(get_workflow_dependencies(os.path.curdir))
