cmake_minimum_required(VERSION 3.13)
project(v8-cmake)

# Extract variables starting with "V8_"

get_cmake_property(V8_CMAKE_VARIABLES VARIABLES)
foreach(V8_CMAKE_VARIABLE ${V8_CMAKE_VARIABLES})
    if (V8_CMAKE_VARIABLE MATCHES "^V8_")
        string(REGEX REPLACE "^V8_(.*)" "\\1" V8_VARIABLE ${V8_CMAKE_VARIABLE})
        string(REGEX REPLACE "_" "-" V8_VARIABLE ${V8_VARIABLE})
        string(TOLOWER ${V8_VARIABLE} V8_VARIABLE)
        set(V8_VARIABLE_VALUE "${${V8_CMAKE_VARIABLE}}")
        if (V8_VARIABLE_VALUE MATCHES "^ON$")
            set(V8_VARIABLE_VALUE "true")
        elseif (V8_VARIABLE_VALUE MATCHES "^OFF$")
            set(V8_VARIABLE_VALUE "false")
        endif()
        set(V8_VARIABLE "--${V8_VARIABLE}=${V8_VARIABLE_VALUE}")
        list(APPEND V8_VARIABLES ${V8_VARIABLE})
    endif()
endforeach()

# Run bootstrap

find_package(Python COMPONENTS Interpreter REQUIRED)
execute_process(
    COMMAND ${Python_EXECUTABLE} "-m" "bootstrap" ${V8_VARIABLES}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    RESULT_VARIABLE V8_BOOTSTRAP_RESULT
)
if (NOT V8_BOOTSTRAP_RESULT EQUAL 0)
    message(FATAL_ERROR "Bootstrap failed")
endif()

# Set variables
set(V8_INCLUDE_DIRS
    "${PROJECT_SOURCE_DIR}/v8"
    "${PROJECT_SOURCE_DIR}/v8/include"
)
set(V8_LIBRARY_DIRS
    "${PROJECT_SOURCE_DIR}/v8/out/${V8_CONFIG_STR}/obj"
)

unset(V8_VARIABLE)
unset(V8_VARIABLES)
unset(V8_VARIABLE_VALUE)
unset(V8_CMAKE_VARIABLE)
unset(V8_CMAKE_VARIABLES)
unset(V8_BOOTSTRAP_RESULT)