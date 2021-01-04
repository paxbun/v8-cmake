# V8 for CMake

Download and Build V8 using CMake automatically.

# Prerequisites

* Visual Studio 2017/2019 with Desktop development with C++
* Debugging Tools for Windows
* gcc or clang (on Ubuntu)
* Python 3
* Python 2.7 (on Ubuntu)
* CMake 3.13 or higher

# Examples

Release mode, Windows

```cmake
set(V8_VERSION "8.7.220.3")
set(V8_CONFIG_STR "x64.release")
set(V8_IS_DEBUG OFF)
set(V8_TARGET_NAME "v8_monolith")
set(V8_IS_COMPONENT_BUILD OFF)
set(V8_IS_CLANG OFF)
set(V8_TARGET_CPU "x64")
set(V8_USE_CUSTOM_LIBCXX OFF)
set(V8_USE_LLD OFF)
set(V8_V8_MONOLITHIC ON)
set(V8_V8_USE_EXTERNAL_STARTUP_DATA OFF)

add_subdirectory(v8-cmake)

target_include_directories(cc3 PRIVATE ${V8_INCLUDE_DIRS})
target_link_directories(cc3 PRIVATE ${V8_LIBRARY_DIRS})
target_link_libraries(cc3 v8_monolith winmm dbghelp)
target_compile_definitions(cc3 PRIVATE -D_ITERATOR_DEBUG_LEVEL=0 ${V8_COMPILE_DEFINITIONS})
```

Release mode, Ubuntu

```cmake
set(V8_VERSION "8.7.220.3")
set(V8_CONFIG_STR "x64.release")
set(V8_IS_DEBUG OFF)
set(V8_TARGET_NAME "v8_monolith")
set(V8_IS_COMPONENT_BUILD OFF)
set(V8_IS_CLANG ON)
set(V8_TARGET_CPU "x64")
set(V8_USE_CUSTOM_LIBCXX OFF)
set(V8_USE_LLD ON)
set(V8_V8_MONOLITHIC ON)
set(V8_V8_USE_EXTERNAL_STARTUP_DATA OFF)

add_subdirectory(v8-cmake)

target_include_directories(cc3 PRIVATE ${V8_INCLUDE_DIRS})
target_link_directories(cc3 PRIVATE ${V8_LIBRARY_DIRS})
target_link_libraries(cc3 v8_monolith pthread)
target_compile_definitions(cc3 PRIVATE ${V8_COMPILE_DEFINITIONS})
```
