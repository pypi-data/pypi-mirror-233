#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ngcore" for configuration "Release"
set_property(TARGET ngcore APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngcore PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/netgen/libngcore.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libngcore.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngcore )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngcore "${_IMPORT_PREFIX}/netgen/libngcore.dylib" )

# Import target "nggui" for configuration "Release"
set_property(TARGET nggui APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nggui PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/netgen/libnggui.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libnggui.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS nggui )
list(APPEND _IMPORT_CHECK_FILES_FOR_nggui "${_IMPORT_PREFIX}/netgen/libnggui.dylib" )

# Import target "ngpy" for configuration "Release"
set_property(TARGET ngpy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngpy PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./netgen/libngpy.so"
  IMPORTED_SONAME_RELEASE "@rpath/libngpy.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngpy )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngpy "${_IMPORT_PREFIX}/./netgen/libngpy.so" )

# Import target "ngguipy" for configuration "Release"
set_property(TARGET ngguipy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngguipy PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./netgen/libngguipy.so"
  IMPORTED_SONAME_RELEASE "@rpath/libngguipy.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngguipy )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngguipy "${_IMPORT_PREFIX}/./netgen/libngguipy.so" )

# Import target "togl" for configuration "Release"
set_property(TARGET togl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(togl PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/netgen/libtogl.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS togl )
list(APPEND _IMPORT_CHECK_FILES_FOR_togl "${_IMPORT_PREFIX}/netgen/libtogl.a" )

# Import target "nglib" for configuration "Release"
set_property(TARGET nglib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nglib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/netgen/libnglib.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libnglib.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS nglib )
list(APPEND _IMPORT_CHECK_FILES_FOR_nglib "${_IMPORT_PREFIX}/netgen/libnglib.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
