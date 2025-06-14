# Copyright 2018 gRPC authors.
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
#
# cmake build file for C++ route_guide example.
# Assumes protobuf and gRPC have been installed using cmake.
# See cmake_externalproject/CMakeLists.txt for all-in-one cmake build
# that automatically builds all the dependencies before building route_guide.

cmake_minimum_required(VERSION 3.16)

project(RouteGuide C CXX)

include(common.cmake)

# Find absl package
find_package(absl CONFIG REQUIRED)

# Proto file

##[[
get_filename_component(rg_proto "../../protos/chat.proto" ABSOLUTE)
get_filename_component(rg_proto_path "${rg_proto}" PATH)

set(rg_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/chat.pb.cc")
set(rg_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/chat.pb.h")
set(rg_grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/chat.grpc.pb.cc")
set(rg_grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/chat.grpc.pb.h")

# Generated sources
add_custom_command(
      OUTPUT "${rg_proto_srcs}" "${rg_proto_hdrs}" "${rg_grpc_srcs}" "${rg_grpc_hdrs}"
      COMMAND ${_PROTOBUF_PROTOC}
      ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
        --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
        -I "${rg_proto_path}"
        --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
        "${rg_proto}"
      DEPENDS "${rg_proto}")
##]]


# Include generated *.pb.h files
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

# rg_grpc_proto
add_library(rg_grpc_proto
  ${rg_grpc_srcs}
  ${rg_grpc_hdrs}
  ${rg_proto_srcs}
  ${rg_proto_hdrs})
target_link_libraries(rg_grpc_proto
  absl::absl_log
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})

# route_guide_helper


# Targets route_guide_(client|server)
foreach(_target
  #route_guide_client route_guide_server
  chatServer
  chatClient
  #route_guide_callback_client route_guide_callback_server
  )
  add_executable(${_target}
    "${_target}.cc")
  target_link_libraries(${_target}
    rg_grpc_proto
    absl::flags_parse
    absl::absl_log
    absl::log_initialize
    absl::log_globals
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF})
endforeach()
