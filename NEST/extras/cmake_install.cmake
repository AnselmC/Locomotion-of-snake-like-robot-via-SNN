# Install script for directory: /home/christoph/nest-simulator-2.14.0-src/extras

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nest/sli" TYPE FILE FILES "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/lib/sli/rcsinfo.sli")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest" TYPE DIRECTORY FILES
    "/home/christoph/nest-simulator-2.14.0-src/extras/bibliography"
    "/home/christoph/nest-simulator-2.14.0-src/extras/logos"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nest" TYPE DIRECTORY FILES "/home/christoph/nest-simulator-2.14.0-src/extras/help_generator")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nest/extras/EditorSupport/emacs" TYPE FILE FILES
    "/home/christoph/nest-simulator-2.14.0-src/extras/EditorSupport/emacs/postscript-sli.el"
    "/home/christoph/nest-simulator-2.14.0-src/extras/EditorSupport/emacs/psvn.el"
    "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/extras/EditorSupport/emacs/sli.el"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nest/extras/EditorSupport/vim/syntax" TYPE FILE FILES "/home/christoph/nest-simulator-2.14.0-src/extras/EditorSupport/vim/syntax/sli.vim")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES
    "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/extras/nest-config"
    "/home/christoph/nest-simulator-2.14.0-src/extras/nest_indirect"
    "/home/christoph/nest-simulator-2.14.0-src/extras/nest_serial"
    "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/extras/nest_vars.sh"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/extras/ConnPlotter/cmake_install.cmake")

endif()

