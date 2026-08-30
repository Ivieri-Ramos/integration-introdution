cmake_minimum_required(VERSION 3.15...3.27)
project(simpson_integration LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(simpson_ext csrc/pybind_module.cpp)

target_include_directories(simpson_ext PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/extern)

target_link_libraries(simpson_ext PRIVATE stdc++)

install(TARGETS simpson_ext DESTINATION .)