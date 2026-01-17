cmake_minimum_required(VERSION 3.10)

# Project Definition
project(IronAgeEngine VERSION 1.0 LANGUAGES CXX)

# Standard: C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optimization Flags (The "Speed" part)
# -O3: Aggressive optimization
# -march=native: Use AVX2 instructions specific to your CPU
add_compile_options(-O3 -march=native -Wall -Wextra -pthread)

# --- Dependencies ---
find_package(PkgConfig REQUIRED)
pkg_check_modules(FFTW3 REQUIRED fftw3)
find_package(GTest REQUIRED)

# --- Include Directories ---
include_directories(
    ${CMAKE_SOURCE_DIR}/cpp/src
    ${FFTW3_INCLUDE_DIRS}
)

# --- Main Engine Executable ---
add_executable(audio_engine cpp/src/main.cpp)
target_link_libraries(audio_engine PRIVATE ${FFTW3_LIBRARIES})

# --- Unit Tests ---
enable_testing()
add_executable(unit_tests cpp/tests/test_main.cpp)
target_link_libraries(unit_tests PRIVATE GTest::gtest GTest::gtest_main ${FFTW3_LIBRARIES})
add_test(NAME core_tests COMMAND unit_tests)