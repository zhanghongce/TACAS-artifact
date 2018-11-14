cmake_minimum_required(VERSION 2.8)

cmake_policy(SET CMP0048 NEW)
project(verilog-parser VERSION 1.0)

#enable_testing()

add_subdirectory(./src)
#add_subdirectory(./docs)

#add_custom_target(verilogparser-test
#    COMMAND ./bin/run-tests.sh
#    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
#    DEPENDS ${EXECUTABLE_NAME}
#    COMMENT "Running Test Suite"
#    VERBATIM
#)
