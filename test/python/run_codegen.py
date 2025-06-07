# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Runs protoc with the gRPC plugin to generate messages and gRPC stubs."""

from grpc_tools import protoc


# get current working directory
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the output directory exists
output_dir = os.path.join(current_dir, "pyproto")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

import sys
sys.path.append(output_dir)

protoc.main(
    (
        "",
        f"-I{current_dir}/../../protos",
        f"--python_out={output_dir}",
        f"--grpc_python_out={output_dir}",
        f"{current_dir}/../../protos/chat.proto",
    )
)
