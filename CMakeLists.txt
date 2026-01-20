cmake_minimum_required(VERSION 3.14)

# Project Definition
project(IronAgeEngine VERSION 1.0 LANGUAGES CXX)

# Standard: C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Optimization Flags
add_compile_options(-O3 -march=native -Wall -Wextra -pthread)

# --- Dependencies ---

# 1. FFTW3 (Math) - Direct Search
find_library(FFTW3_LIB fftw3 REQUIRED)
find_path(FFTW3_INC fftw3.h REQUIRED)

# 2. GoogleTest (Testing) - FetchContent (The Fix)
# Instead of looking for a broken system install, we download and build it.
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
# Prevent GTest from overriding our compiler settings (Windows/Visual Studio specific, but good practice)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# --- Include Directories ---
include_directories(
    ${CMAKE_SOURCE_DIR}/cpp/src
    ${FFTW3_INC}
)

# --- Main Engine Executable ---
add_executable(audio_engine cpp/src/main.cpp)
target_link_libraries(audio_engine PRIVATE ${FFTW3_LIB})

# --- Unit Tests ---
enable_testing()
add_executable(unit_tests cpp/tests/test_main.cpp)

# Link against the target we just built (gtest_main handles the main() function automatically)
target_link_libraries(unit_tests PRIVATE gtest_main ${FFTW3_LIB})

# Register the test
include(GoogleTest)
gtest_discover_tests(unit_tests)