# Install script for directory: /home/christoph/nest-simulator-2.14.0-src/pynest

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
  execute_process(
    COMMAND /usr/bin/python setup.py build --build-base=/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/pynest/build
                               install --prefix=/home/christoph/nest-simulator-2.14.0
                                       --install-lib=/home/christoph/nest-simulator-2.14.0/lib/python2.7/site-packages
                                       --install-scripts=/home/christoph/nest-simulator-2.14.0/bin
                                       --install-data=/home/christoph/nest-simulator-2.14.0/share/nest
    WORKING_DIRECTORY "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/pynest")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python2.7/site-packages/nest/pynestkernel.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python2.7/site-packages/nest/pynestkernel.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python2.7/site-packages/nest/pynestkernel.so"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/site-packages/nest" TYPE MODULE FILES "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/pynest/pynestkernel.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python2.7/site-packages/nest/pynestkernel.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python2.7/site-packages/nest/pynestkernel.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python2.7/site-packages/nest/pynestkernel.so"
         OLD_RPATH "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/nest:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/models:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/precise:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/topology:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/nestkernel:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/librandom:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/sli:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/libnestutil:"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python2.7/site-packages/nest/pynestkernel.so")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nest/extras" TYPE FILE FILES "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/pynest/do_tests.py")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/examples/pynest" TYPE DIRECTORY FILES "/home/christoph/nest-simulator-2.14.0-src/pynest/examples/")
endif()

