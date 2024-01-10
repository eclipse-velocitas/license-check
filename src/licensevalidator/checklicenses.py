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

"""Provides methods and classes to check licenses of a software project."""

from io import open

from licensevalidator.lib.dependency import DependencyInfo


class LicenseValidator:
    """
    summary: Validator for licenses.

    Can be configured to either operate on a whitelist or a blacklist.
    """

    def __init__(
        self, licenses_list: list[str], is_licenses_list_inclusive: bool = True
    ):
        """Instantiate a new LicenseValidator.

        Args:
            licenses_list (list[str]): The list of licenses.
            is_licenses_list_inclusive (bool, optional):
                If set to True the licenses_list is a whitelist.
                If set to False the licenses_list is a blacklist.
                Defaults to True.
        """
        self.licenses_list = licenses_list
        self.is_licenses_list_inclusive = is_licenses_list_inclusive

    def is_license_valid(self, license_name: str) -> bool:
        """Return if the given license is valid.

        Args:
            license_name (str):
                The name of the license to check.

        Returns:
            bool: True if the license is valid. False otherwise.
        """
        contained_in_list = license_name in self.licenses_list

        # containedInList    | inclusive | result
        # true                 true        true
        # false                true        false
        # true                 false       false
        # false                false       true
        if not contained_in_list:
            # give it another try without the " License" suffix
            if license_name is not None:
                contained_in_list = (
                    license_name.replace(" License", "") in self.licenses_list
                )
        return contained_in_list == self.is_licenses_list_inclusive


def read_license_list(path: str) -> list[str]:
    """Read the file at the given path.

    Args:
        path (str):
            The path to the license list file to read.

    Returns:
        list[str]: The contents of the license list.
    """
    result = []
    with open(path, "r", encoding="utf-8") as file:
        while (line := file.readline()) != "":
            result.append(line.strip())

    return result


def check_licenses(
    origin: str,
    all_deps_with_licenses: list[DependencyInfo],
    whitelisted_licenses: list[str],
) -> bool:
    """Check if all given licenses are present in the provided whitelist.

    Args:
        origin (str):
            Origin of the dependencies.
        all_deps_with_licenses (list[DependencyInfo]):
            The list of all dependencies along with their licenses.
        whitelisted_licenses (list[str]):
            The list of whitelisted licenses.

    Returns:
        bool: True if all licenses are present in the whitelist.
              False otherwise.
    """
    validator = LicenseValidator(whitelisted_licenses, True)

    result = True
    print(f'Checking licenses from "{origin}"...')
    for dep_info in all_deps_with_licenses:
        print(f'\t"{dep_info.name}" version "{dep_info.version}" uses licenses:')
        if len(dep_info.licenses) > 0:
            for license_name in dep_info.licenses:
                print(f'\t\t"{license_name}" -> ', end="")
                if not validator.is_license_valid(license_name):
                    result = False
                    print("Not OK")
                else:
                    print("OK")
        else:
            result = False
            print('\t"No license available!" -> ', end="")
    return result
