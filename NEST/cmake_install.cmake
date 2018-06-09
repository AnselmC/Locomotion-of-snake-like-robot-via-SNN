# Install script for directory: /home/christoph/nest-simulator-2.14.0-src

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest" TYPE FILE FILES
    "/home/christoph/nest-simulator-2.14.0-src/LICENSE"
    "/home/christoph/nest-simulator-2.14.0-src/README.md"
    "/home/christoph/nest-simulator-2.14.0-src/NEWS"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/doc/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/examples/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/extras/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/lib/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/libnestutil/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/librandom/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/models/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/sli/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/nest/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/nestkernel/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/precise/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/topology/cmake_install.cmake")
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/pynest/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
