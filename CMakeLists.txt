cmake_minimum_required(VERSION 3.20)

project(slc-grpc-lib)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(slc-grpc-lib)

find_package(gRPC REQUIRED CONFIG)
find_package(Protobuf REQUIRED CONFIG)
find_package(CLI11 CONFIG REQUIRED)
include_directories(SYSTEM ${gRPC_INCLUDE_DIRS})

add_subdirectory(test/cpp)