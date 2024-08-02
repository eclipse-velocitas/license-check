# Copyright (c) 2022-2024 Contributors to the Eclipse Foundation
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

"""Integration tests for license validator."""


from licensevalidator.licensevalidator import validate_used_licenses


def test_python_with_workflows():
    """Test python project without workflows."""
    result, origin_vs_deps = validate_used_licenses(
        "./testbench/python-with-workflows",
        [
            {
                "path": "./my-source",
                "python-pip-included-requirement-files": ["requirements.txt"],
            }
        ],
        "whitelist.txt",
    )

    assert result is True
    assert len(origin_vs_deps) == 2

    assert "Python" in origin_vs_deps
    python_deps = origin_vs_deps["Python"]
    assert len(python_deps) == 4
    assert python_deps[0].name == "idna"
    assert python_deps[1].name == "multidict"
    assert python_deps[2].name == "six"
    assert python_deps[3].name == "yarl"

    assert "Workflows" in origin_vs_deps
    workflow_deps = origin_vs_deps["Workflows"]
    assert workflow_deps[0].name == "actions/checkout"


def test_python_without_workflows():
    """Test python project with workflows."""
    result, origin_vs_deps = validate_used_licenses(
        "./testbench/python-without-workflows",
        [
            {
                "path": "./src",
                "python-pip-included-requirement-files": ["requirements.txt"],
            }
        ],
        "whitelist.txt",
    )

    assert result is True
    assert len(origin_vs_deps) == 1
    assert "Python" in origin_vs_deps
    python_deps = origin_vs_deps["Python"]
    assert len(python_deps) == 4
    assert python_deps[0].name == "idna"
    assert python_deps[1].name == "multidict"
    assert python_deps[2].name == "six"
    assert python_deps[3].name == "yarl"


def test_python_without_req_files():
    """Test python project with non-existant requirement file."""
    result, origin_vs_deps = validate_used_licenses(
        "./testbench/python-without-workflows",
        [
            {
                "path": "./src",
                "python-pip-included-requirement-files": ["random-string.txt"],
            }
        ],
        "whitelist.txt",
    )

    assert result is True
    assert len(origin_vs_deps) == 0


def test_javascript():
    """Test javascript project."""
    result, origin_vs_deps = validate_used_licenses(
        "./testbench/javascript-npm", [{"path": "."}], "whitelist.txt"
    )

    assert result is True
    assert len(origin_vs_deps) == 1
    assert "JavaScript" in origin_vs_deps

    assert origin_vs_deps["JavaScript"][0].name == "javascript-npm"
    assert origin_vs_deps["JavaScript"][0].version == "1.0.0"
    assert origin_vs_deps["JavaScript"][1].name == "typescript"
    assert origin_vs_deps["JavaScript"][1].version == "4.6.3"


# def test_cpp():
#     """Test cpp project."""
#     result, origin_vs_deps = validate_used_licenses(
#         "./testbench/multilang/cpp-proj",
#         [{"path": ".", "cpp-conan-included-profile-files": ["./conan_profile"]}],
#         "../whitelist.txt",
#     )

#     assert result
#     assert len(origin_vs_deps) == 1
#     assert "c++" in origin_vs_deps

#     index = 0
#     assert origin_vs_deps["c++"][index].name == "abseil"

#     index += 1
#     assert origin_vs_deps["c++"][index].name == "c-ares"

#     index += 1
#     assert origin_vs_deps["c++"][index].name == "grpc"

#     index += 1
#     assert origin_vs_deps["c++"][index].name == "gtest"

#     index += 1
#     assert origin_vs_deps["c++"][index].name == "openssl"

#     index += 1
#     assert origin_vs_deps["c++"][index].name == "protobuf"

#     index += 1
#     assert origin_vs_deps["c++"][index].name == "re2"

#     index += 1
#     assert origin_vs_deps["c++"][index].name == "zlib"


# def test_multilang():
#     result, origin_vs_deps = validate_used_licenses(
#         "./testbench/multilang",
#         [
#             {"path": "cpp-proj", "cpp-conan-included-profile-files": ["conan_profile"]},
#             {"path": "rust-proj"},
#             {"path": "python-proj"},
#         ],
#         "whitelist.txt",
#     )

#     assert result is False
#     assert len(origin_vs_deps) == 3
#     assert "c++" in origin_vs_deps
#     assert "Rust" in origin_vs_deps
#     assert "Python" in origin_vs_deps
