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


FROM python:3.10.3-slim

ARG DEBIAN_FRONTEND=noninteractive

COPY ./src/ /

# Update packages & install license finder
RUN apt update \
    && apt install -y git \
    && apt install -y ruby \
    && gem install license_finder -v 7.1.0 \
    && pip3 install -r /requirements.txt

# Install conan to handle c++ dependencies
RUN pip3 install -U conan

# Install cargo to handle Rust dependencies
RUN apt install -y curl && curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install npm to handle JavaScript dependencies
RUN apt install -y npm

# WORKAROUND: GitHub sets the HOME variable when starting the container this makes these folders
# created at container image build time unavailable
ENV CONAN_USER_HOME=/root
ENV CARGO_HOME=/root/.cargo
ENV RUSTUP_HOME=/root/.rustup

# Run the Python3 Github Action wrapper
ENTRYPOINT ["python3", "-u", "/action.py"]
