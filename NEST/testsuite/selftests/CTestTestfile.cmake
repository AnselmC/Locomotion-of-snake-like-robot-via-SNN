# CMake generated Testfile for 
# Source directory: /home/christoph/nest-simulator-2.14.0-src/testsuite/selftests
# Build directory: /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/testsuite/selftests
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(selftests/test_pass.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_pass.sli")
add_test(selftests/test_goodhandler.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_goodhandler.sli")
add_test(selftests/test_lazyhandler.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_lazyhandler.sli")
add_test(selftests/test_fail.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_fail.sli")
set_tests_properties(selftests/test_fail.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_stop.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_stop.sli")
set_tests_properties(selftests/test_stop.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_badhandler.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_badhandler.sli")
set_tests_properties(selftests/test_badhandler.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_pass_or_die.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_pass_or_die.sli")
set_tests_properties(selftests/test_pass_or_die.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_assert_or_die_b.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_assert_or_die_b.sli")
set_tests_properties(selftests/test_assert_or_die_b.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_assert_or_die_p.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_assert_or_die_p.sli")
set_tests_properties(selftests/test_assert_or_die_p.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_fail_or_die.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_fail_or_die.sli")
set_tests_properties(selftests/test_fail_or_die.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_crash_or_die.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_crash_or_die.sli")
set_tests_properties(selftests/test_crash_or_die.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_failbutnocrash_or_die_crash.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_failbutnocrash_or_die_crash.sli")
set_tests_properties(selftests/test_failbutnocrash_or_die_crash.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_failbutnocrash_or_die_pass.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_failbutnocrash_or_die_pass.sli")
set_tests_properties(selftests/test_failbutnocrash_or_die_pass.sli PROPERTIES  WILL_FAIL "TRUE")
add_test(selftests/test_passorfailbutnocrash_or_die.sli "/home/christoph/nest-simulator-2.14.0/bin/nest" "/home/christoph/nest-simulator-2.14.0/share/doc/nest/selftests/test_passorfailbutnocrash_or_die.sli")
set_tests_properties(selftests/test_passorfailbutnocrash_or_die.sli PROPERTIES  WILL_FAIL "TRUE")
