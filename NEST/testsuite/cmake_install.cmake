# Install script for directory: /home/christoph/nest-simulator-2.14.0-src/testsuite

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/christoph/nest-simulator-2.14.0")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest" TYPE DIRECTORY FILES
    "/home/christoph/nest-simulator-2.14.0-src/testsuite/selftests"
    "/home/christoph/nest-simulator-2.14.0-src/testsuite/unittests"
    "/home/christoph/nest-simulator-2.14.0-src/testsuite/regressiontests"
    "/home/christoph/nest-simulator-2.14.0-src/testsuite/mpitests"
    "/home/christoph/nest-simulator-2.14.0-src/testsuite/mpi_selftests"
    "/home/christoph/nest-simulator-2.14.0-src/testsuite/musictests"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nest/extras" TYPE PROGRAM FILES "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/do_tests.sh")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/selftests/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/unittests/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/regressiontests/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/mpi_selftests/fail/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/mpi_selftests/pass/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/mpitests/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/musictests/cmake_install.cmake")

endif()

