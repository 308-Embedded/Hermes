
function(DECLARE_LIB LIB_NAME UUID HEADER SOURCE_FILE COMPILE_OPTION LINK_OPTION)

    # UUID Duplication is not allowed.
    list(FIND GLOBAL_LIBRARIES ${UUID} index)
    if(index GREATER -1)
        message(FATAL_ERROR "Library UUID '${UUID}' already exists!")
    else()
        list(APPEND GLOBAL_LIBRARIES "${UUID}")
        set(GLOBAL_LIBRARIES "${GLOBAL_LIBRARIES}" CACHE STRING "global libraries" FORCE)
    endif()

    set(${UUID}_LIB_NAME "${LIB_NAME}" CACHE STRING "Library name for ${UUID}" FORCE)
    set(${UUID}_HEADER "${HEADER}" CACHE STRING "Header file for ${UUID}" FORCE)
    set(${UUID}_SOURCE_FILE "${SOURCE_FILE}" CACHE STRING "Source file for ${UUID}" FORCE)
    set(${UUID}_COMPILE_OPTION "${COMPILE_OPTION}" CACHE STRING "Compile options for ${UUID}" FORCE)
    set(${UUID}_LINK_OPTION "${LINK_OPTION}" CACHE STRING "Link options for ${UUID}" FORCE)

    # Create maps between lib_name to uuid
    if(NOT DEFINED ${LIB_NAME}_UUIDS)
    set(${LIB_NAME}_UUIDS "" CACHE STRING "Mapping of UUIDs for ${LIB_NAME}" FORCE)
    endif()

    list(FIND ${LIB_NAME}_UUIDS ${UUID} index)
    if(index GREATER -1)
        # message(STATUS "UUID '${UUID}' already exists in the list!")
    else()
        list(APPEND ${LIB_NAME}_UUIDS "${UUID}")
        set(${LIB_NAME}_UUIDS "${${LIB_NAME}_UUIDS}" CACHE STRING "Mapping of UUIDs for ${LIB_NAME}" FORCE)
    endif()

    message(STATUS "Library ${LIB_NAME} created with UUID: ${UUID}")

endfunction()

# compile libraries listed in GLOBAL_LIBRARIES
function(COMPILE_ALL_LIBS)

    foreach(UUID ${GLOBAL_LIBRARIES})
        add_library(${UUID} STATIC ${${UUID}_SOURCE_FILE})
        set_target_properties(${UUID} PROPERTIES OUTPUT_NAME "${${UUID}_LIB_NAME}")
        target_include_directories(${UUID} PRIVATE ${${UUID}_HEADER})
        target_compile_options(${UUID} PRIVATE ${${UUID}_COMPILE_OPTION})
        target_link_libraries(${UUID} PRIVATE ${${UUID}_LINK_OPTION})
        message(STATUS "Compiling library: ${${UUID}_LIB_NAME}")
    endforeach()

endfunction()