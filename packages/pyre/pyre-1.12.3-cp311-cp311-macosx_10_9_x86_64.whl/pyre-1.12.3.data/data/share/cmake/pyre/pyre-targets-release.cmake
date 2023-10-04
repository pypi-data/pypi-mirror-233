#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "pyre::journal" for configuration "Release"
set_property(TARGET pyre::journal APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(pyre::journal PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libjournal.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libjournal.dylib"
  )

list(APPEND _cmake_import_check_targets pyre::journal )
list(APPEND _cmake_import_check_files_for_pyre::journal "${_IMPORT_PREFIX}/lib/libjournal.dylib" )

# Import target "pyre::pyre" for configuration "Release"
set_property(TARGET pyre::pyre APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(pyre::pyre PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libpyre.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libpyre.dylib"
  )

list(APPEND _cmake_import_check_targets pyre::pyre )
list(APPEND _cmake_import_check_files_for_pyre::pyre "${_IMPORT_PREFIX}/lib/libpyre.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
