# Copyright (c) 2023-2024 Contributors to the Eclipse Foundation
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

import os
import shutil
import subprocess
import pathlib

from git import Repo

from action import is_dirty, read_config_file

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()


def test_parse_directory_configs():
    """Test good case"""
    config = read_config_file("./testbench/multilang/.lc.config.yml")

    assert config is not None
    assert len(config["scan-dirs"]) == 3


def test_no_commit_if_not_dirty():
    """Test no commit created if file is not dirty"""
    repo_root = os.path.join(ROOT_DIR, "testbench/git")
    notice_file_name = "my-notice-file.md"
    notice_file_path = os.path.join(repo_root, notice_file_name)
    # init repo
    repo = Repo.init(repo_root)
    subprocess.run(
        [
            "git",
            "config",
            "--global",
            "--add",
            "safe.directory",
            repo_root,
        ]
    )

    # create file
    with open(notice_file_path, "w+", encoding="utf-8") as notice_file:
        notice_file.write("first license")

    # add file initially
    repo.index.add(notice_file_name)
    repo.index.commit("Initial")

    ref_log = repo.active_branch.log()

    try:
        assert not is_dirty(repo_root, notice_file_name)
        assert len(ref_log) == 1
        assert ref_log[0].message == "commit (initial): Initial"
    finally:
        os.remove(notice_file_path)
        shutil.rmtree(os.path.join(repo_root, ".git"))
        subprocess.run(
            [
                "git",
                "config",
                "--global",
                "--add",
                "safe.directory",
                ROOT_DIR,
            ]
        )


def test_commit_if_dirty():
    """Test commit is created if file is dirty"""
    repo_root = os.path.join(ROOT_DIR, "testbench/git")
    notice_file_name = "my-notice-file.md"
    notice_file_path = os.path.join(repo_root, notice_file_name)

    # init repo
    repo = Repo.init(repo_root)
    subprocess.run(
        [
            "git",
            "config",
            "--global",
            "--add",
            "safe.directory",
            repo_root,
        ]
    )

    # create file
    with open(notice_file_path, "w+", encoding="utf-8") as notice_file:
        notice_file.write("first license")

    # add file initially
    repo.index.add([notice_file_name])
    repo.index.commit("Initial")

    # modify file
    with open(notice_file_path, "a", encoding="utf-8") as notice_file:
        notice_file.write("new license")

    ref_log = repo.active_branch.log()

    try:
        assert is_dirty(repo_root, notice_file_name)
        assert len(ref_log) == 1
        assert ref_log[0].message == "commit (initial): Initial"
    finally:
        os.remove(notice_file_path)
        shutil.rmtree(os.path.join(repo_root, ".git"))
        subprocess.run(
            [
                "git",
                "config",
                "--global",
                "--add",
                "safe.directory",
                ROOT_DIR,
            ]
        )
