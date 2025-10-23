cmake_minimum_required(VERSION 3.21)
project(Hermes)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(library_manager)

set(GLOBAL_LIBRARIES "" CACHE STRING "List of libraries" FORCE) # Record All libraries to be compiled

add_subdirectory(CommonPkg)

COMPILE_ALL_LIBS()