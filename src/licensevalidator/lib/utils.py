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

"""Provides utility methods required by various modules."""


def print_step(step_description: str) -> None:
    """Pretty-prints the step description passed to the method to stdout.

    Args:
        step_description (str): A textual description of the step.
    """
    print("##########################################################")
    print(f"### {step_description:<50} ###")
    print("##########################################################")
