# CMake generated Testfile for 
# Source directory: /home/christoph/nest-simulator-2.14.0-src/pynest
# Build directory: /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/pynest
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(PyNEST "/usr/bin/nosetests" "-v" "--with-xunit" "--xunit-file=/home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/reports/pynest_tests.xml" "/home/christoph/nest-simulator-2.14.0/lib/python2.7/site-packages/nest/tests")
