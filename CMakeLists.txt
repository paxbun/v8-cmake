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
file(
    READ "${V8_ROOT}/config/definitions.${V8_CONFIG_STR}.txt"
    V8_COMPILE_DEFINITIONS
)
set(V8_COMPILE_DEFINITIONS ${V8_COMPILE_DEFINITIONS} PARENT_SCOPE)


# Set variables
set(V8_INCLUDE_DIRS
    "${V8_ROOT}/v8"
    "${V8_ROOT}/v8/include"
    PARENT_SCOPE
)
set(V8_LIBRARY_DIRS
    "${V8_ROOT}/v8/out/${V8_CONFIG_STR}/obj"
    PARENT_SCOPE
)

# Change runtime options
set(V8_COMPILER_FLAGS
    CMAKE_CXX_FLAGS
    CMAKE_CXX_FLAGS_DEBUG
    CMAKE_CXX_FLAGS_RELEASE
    CMAKE_CXX_FLAGS_MINSIZEREL
    CMAKE_CXX_FLAGS_RELWITHDEBINFO
    CMAKE_C_FLAGS
    CMAKE_C_FLAGS_DEBUG
    CMAKE_C_FLAGS_RELEASE
    CMAKE_C_FLAGS_MINSIZEREL
    CMAKE_C_FLAGS_RELWITHDEBINFO
)
foreach(V8_COMPILER_FLAG ${V8_COMPILER_FLAGS})
    string(REPLACE "/MD" "/MT" ${V8_COMPILER_FLAG} "${${V8_COMPILER_FLAG}}")
    set(${V8_COMPILER_FLAG} "${${V8_COMPILER_FLAG}}" PARENT_SCOPE)
endforeach()