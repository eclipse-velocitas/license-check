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
import sys

from git import Repo

sys.path.append("./src")

from action import commit_notice_file_if_dirty, read_config_file


def test_parse_directory_configs():
    """Test good case"""
    config = read_config_file("./testbench/multilang/.lc.config.yml")

    assert config is not None
    assert len(config["scan-dirs"]) == 3


def test_no_commit_if_not_dirty():
    """Test no commit created if file is not dirty"""
    notice_file_path = "./testbench/git/my-notice-file.md"

    # init repo
    repo = Repo.init("./testbench/git")

    # create file
    with open(notice_file_path, "w+", encoding="utf-8") as notice_file:
        notice_file.write("first license")

    # add file initially
    repo.index.add("my-notice-file.md")
    repo.index.commit("Initial")

    commit_notice_file_if_dirty("./testbench/git/", "my-notice-file")
    ref_log = repo.active_branch.log()

    try:
        assert len(ref_log) == 1
        assert ref_log[0].message == "commit (initial): Initial"
    finally:
        os.remove(notice_file_path)
        shutil.rmtree("./testbench/git/.git")


def test_commit_if_dirty():
    """Test commit is created if file is dirty"""
    notice_file_path = "./testbench/git/my-notice-file.md"

    # init repo
    repo = Repo.init("./testbench/git")

    # create file
    with open(notice_file_path, "w+", encoding="utf-8") as notice_file:
        notice_file.write("first license")

    # add file initially
    repo.index.add("my-notice-file.md")
    repo.index.commit("Initial")

    # modify file
    with open(notice_file_path, "w+", encoding="utf-8") as notice_file:
        notice_file.write("new license")

    commit_notice_file_if_dirty("./testbench/git/", "my-notice-file", push=False)
    ref_log = repo.active_branch.log()

    try:
        assert len(ref_log) == 2
        assert ref_log[0].message == "commit (initial): Initial"
        assert ref_log[1].message == "Update my-notice-file.md"
    finally:
        os.remove(notice_file_path)
        shutil.rmtree("./testbench/git/.git")
