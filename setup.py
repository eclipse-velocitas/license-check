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

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("src/requirements.txt", encoding="utf-8") as reqs_file:
    requirements = reqs_file.read().splitlines()

setuptools.setup(
    name="licensevalidator",
    version="1.2.3",
    description="A validator for dependency licenses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eclipse-velocitas/license-check",
    packages=["licensevalidator", "licensevalidator.lib", "dash"],
    package_data={"licensevalidator": ["py.typed"]},
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
)
