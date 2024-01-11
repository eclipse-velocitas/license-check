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

"""Contains classes and methods to model dependencies."""


class DependencyInfo:
    """Describes a single dependency of a software project."""

    def __init__(self, name: str, version: str, licenses: list[str]):
        """Create a new instance.

        Args:
            name (str): Name of the dependency.
            version (str): Version of the dependency.
            licenses (list[str]): List of license names.
        """
        self.name = name
        self.version = version
        self.licenses = licenses

    def __repr__(self) -> str:
        return f"DependencyInfo({self.name}, {self.version}, {self.licenses.__str__()})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DependencyInfo):
            return False

        return (
            self.name == other.name
            and self.version == other.version
            and self.licenses == other.licenses
        )

    def __hash__(self) -> int:
        return hash(self.__repr__())
