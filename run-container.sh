#!/usr/bin/env bash
#********************************************************************************
#* Copyright (c) 2021 Contributors to the Eclipse Foundation
#*
#* See the NOTICE file(s) distributed with this work for additional
#* information regarding copyright ownership.
#*
#* This program and the accompanying materials are made available under the
#* terms of the Eclipse Public License 2.0 which is available at
#* http://www.eclipse.org/legal/epl-2.0
#*
#* SPDX-License-Identifier: EPL-2.0
#********************************************************************************/

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

docker build . -t license-checker:latest && docker run --workdir /github/workspace -v "${SCRIPT_DIR}/testbench/multilang":"/github/workspace" --rm license-checker:latest \
    "true" "NOTICE-GENERATED" false ".lc.config.yml"
