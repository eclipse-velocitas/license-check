#!/usr/bin/env bash
# Copyright (c) 2022-2026 Contributors to the Eclipse Foundation
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

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

GEM_NAME=license_finder
GEM_VERSION=7.2.1

mkdir -p patch_$GEM_NAME && cd $_

echo "### CLONE ###"
git clone --depth 1 --branch v$GEM_VERSION https://github.com/pivotal/LicenseFinder.git
cd LicenseFinder
read -p "Press enter to continue"

echo "### PATCH ###"
patch -p1 -i $SCRIPT_DIR/$GEM_NAME-$GEM_VERSION.patch
read -p "Press enter to continue"

echo "### BUILD ###"
gem build $GEM_NAME.gemspec
read -p "Press enter to continue"

echo "### INSTALL ###"
sudo gem install ./$GEM_NAME-$GEM_VERSION.gem
