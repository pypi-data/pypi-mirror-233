# Install script for directory: /Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
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

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/libkj.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj.a")
    execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kj" TYPE FILE FILES
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/common.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/units.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/memory.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/refcount.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/array.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/vector.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/string.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/string-tree.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/exception.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/debug.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/arena.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/miniposix.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/io.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/tuple.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/one-of.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/function.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/mutex.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/thread.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/threadlocal.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/main.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/windows-sanity.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kj/parse" TYPE FILE FILES
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/parse/common.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/parse/char.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kj/std" TYPE FILE FILES "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/std/iostream.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/libkj-test.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-test.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-test.a")
    execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-test.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kj" TYPE FILE FILES "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/test.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kj/compat" TYPE FILE FILES "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/compat/gtest.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/libkj-async.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-async.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-async.a")
    execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-async.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kj" TYPE FILE FILES
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/async-prelude.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/async.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/async-inl.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/async-unix.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/async-win32.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/async-io.h"
    "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/time.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/libkj-http.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-http.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-http.a")
    execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkj-http.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kj/compat" TYPE FILE FILES "/Users/zackbeucler/Desktop/stable-retro/third-party/capnproto/c++/src/kj/compat/http.h")
endif()

