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
