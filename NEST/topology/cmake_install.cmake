# Install script for directory: /home/christoph/nest-simulator-2.14.0-src/topology

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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/topology/libtopology.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so"
         OLD_RPATH "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/nestkernel:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/librandom:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/sli:/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/libnestutil:"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nest/sli" TYPE FILE FILES "/home/christoph/nest-simulator-2.14.0-src/topology/sli/topology-interface.sli")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/topology" TYPE FILE FILES "/home/christoph/nest-simulator-2.14.0-src/topology/doc/Topology_UserManual.pdf")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/topology/unittests" TYPE FILE FILES
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_donut_anchor_11.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_rect_01.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_rect_10.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_circ_anchor_00.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_03.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_donut_anchor_10.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_11.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_circ_anchor_10.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_circ_anchor_00.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_15.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_rect_11.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_weight_delay.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_05.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_rect_00.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_donut_anchor_11.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_02.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_weight_delay_free.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_06.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_10.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_distance.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_04.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_donut_anchor_01.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_01.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_rect_11.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_00.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_donut_anchor_01.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_rows_cols_pos.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_oversize_mask.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_circ_anchor_11.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_rect_02.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_rect_00.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_donut_anchor_00.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_circ_anchor_11.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_donut_anchor_00.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_rect_13.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_circ_anchor_01.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_circ_anchor_10.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_rect_01.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_reg_mask_grid_anchor_13.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_circ_anchor_01.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/unittests/test_free_mask_donut_anchor_10.sli"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/topology/mpitests" TYPE FILE FILES
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/mpitests/topo_mpi_test_convergent.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/mpitests/topo_mpi_test_divergent.sli"
    "/home/christoph/nest-simulator-2.14.0-src/topology/testsuite/mpitests/ticket-516.sli"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  execute_process(
    COMMAND /usr/bin/python setup.py build --build-base=/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/topology/build
                               install --prefix=/home/christoph/nest-simulator-2.14.0
                                       --install-lib=/home/christoph/nest-simulator-2.14.0/lib/python2.7/site-packages
                                       --install-scripts=/home/christoph/nest-simulator-2.14.0/bin
                                       --install-data=/home/christoph/nest-simulator-2.14.0/share/nest
    WORKING_DIRECTORY "/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/topology")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/examples/topology" TYPE FILE FILES
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/conncon_targets.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/grid_iaf_oc.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/connex.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/gaussex.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/connex_ew.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/conncon_sources.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/test_3d_gauss.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/grid_iaf.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/conncomp.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/hill_tononi_Vp.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/test_3d.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/README"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/grid_iaf_irr.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/test_3d_exp.py"
    "/home/christoph/nest-simulator-2.14.0-src/topology/examples/ctx_2n.py"
    )
endif()

