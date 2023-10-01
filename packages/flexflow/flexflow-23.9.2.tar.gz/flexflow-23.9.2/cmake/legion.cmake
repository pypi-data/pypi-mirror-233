if(FF_USE_EXTERNAL_LEGION)
	if(NOT "${LEGION_ROOT}" STREQUAL "")
    set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} ${LEGION_ROOT}/share/Legion/cmake)
	endif()
	find_package(Legion REQUIRED)
	get_target_property(LEGION_INCLUDE_DIRS Legion::RealmRuntime INTERFACE_INCLUDE_DIRECTORIES)
	string(REGEX REPLACE "/include" "" LEGION_ROOT_TMP ${LEGION_INCLUDE_DIRS})
	if("${LEGION_ROOT}" STREQUAL "")
		set(LEGION_ROOT ${LEGION_ROOT_TMP})
	else()
		if(NOT "${LEGION_ROOT}" STREQUAL ${LEGION_ROOT_TMP})
			message( FATAL_ERROR "LEGION_ROOT is not set correctly ${LEGION_ROOT} ${LEGION_ROOT_TMP}")
		endif()
	endif()
	message(STATUS "Use external Legion cmake found: ${LEGION_ROOT_TMP}")
	message(STATUS "Use external Legion: ${LEGION_ROOT}")
	set(LEGION_LIBRARY Legion::Legion)
else()
	# Check availability of precompiled Legion library
	set(LEGION_URL "")
	if((FF_USE_PREBUILT_LEGION OR FF_USE_ALL_PREBUILT_LIBRARIES) AND CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "x86_64" AND 
		FF_USE_PYTHON AND NOT "${FF_LEGION_NETWORKS}" STREQUAL "gasnet" AND FF_MAX_DIM EQUAL 5)
		# For now, reusing pre-compiled Legion library only works when the Python library on the target machine 
		# is stored at the path `/opt/conda/lib/libpython3.10.so`. Here, we check if this is the case.
		find_package(PythonInterp)
  		find_package(PythonLibs)
		if(PYTHON_LIBRARIES STREQUAL "/opt/conda/lib/libpython3.10.so")
			if(LINUX_VERSION MATCHES "20.04")
				if (FF_GPU_BACKEND STREQUAL "cuda")
					if (CUDA_VERSION VERSION_EQUAL "11.0")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_11.0.3.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.1")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_11.1.1.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.2")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_11.2.2.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.3")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_11.3.1.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.4")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_11.4.3.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.5")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_11.5.2.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.6")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_11.6.2.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.7")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_11.7.0.tar.gz")
					endif()
				elseif(FF_GPU_BACKEND STREQUAL "hip_rocm")
					set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-20.04_hip_rocm.tar.gz")
				endif()
			  elseif(LINUX_VERSION MATCHES "18.04")
			  	if (FF_GPU_BACKEND STREQUAL "cuda")
					if (CUDA_VERSION VERSION_EQUAL "10.1")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_10.1.243.tar.gz")
					elseif (CUDA_VERSION VERSION_EQUAL "10.2")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_10.2.89.tar.gz")
					elseif (CUDA_VERSION VERSION_EQUAL "11.0")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_11.0.3.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.1")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_11.1.1.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.2")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_11.2.2.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.3")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_11.3.1.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.4")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_11.4.3.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.5")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_11.5.2.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.6")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_11.6.2.tar.gz")
					elseif(CUDA_VERSION VERSION_EQUAL "11.7")
					  set(LEGION_URL "https://github.com/flexflow/flexflow-third-party/releases/latest/download/legion_ubuntu-18.04_11.7.0.tar.gz")
					endif()
				endif()
			  endif()
		endif()
	endif()

	if(LEGION_URL)
		# Download and import pre-compiled Legion library
		message(STATUS "Using pre-compiled Legion library")
		message(STATUS "LEGION_URL: ${LEGION_URL}")
		set(LEGION_NAME legion)
		set(LEGION_LIBRARY legion)
		set(REALM_LIBRARY realm)

		include(FetchContent)
		FetchContent_Declare(${LEGION_NAME}
			URL ${LEGION_URL}
			CONFIGURE_COMMAND ""
			BUILD_COMMAND ""
		)
		FetchContent_GetProperties(${LEGION_NAME})
		if(NOT ${LEGION_NAME}_POPULATED)
			FetchContent_Populate(${LEGION_NAME})
		endif()
		
		set(LEGION_FOLDER_PATH ${${LEGION_NAME}_SOURCE_DIR}/export/${LEGION_NAME})
		SET(LEGION_INCLUDE_DIR ${LEGION_FOLDER_PATH}/include)
		SET(LEGION_DEF_DIR ${LEGION_INCLUDE_DIR})
		SET(LEGION_BIN_DIR ${LEGION_FOLDER_PATH}/bin/)
		SET(LEGION_LIB_DIR ${LEGION_FOLDER_PATH}/lib)
		SET(LEGION_SHARE_DIR ${LEGION_FOLDER_PATH}/share/)
		message(STATUS "Legion library path: ${LEGION_FOLDER_PATH}")

		add_library(${LEGION_LIBRARY} SHARED IMPORTED)
		add_library(${REALM_LIBRARY} SHARED IMPORTED)
		set_target_properties(${LEGION_LIBRARY} PROPERTIES IMPORTED_LOCATION ${LEGION_LIB_DIR}/liblegion${LIBEXT})
		set_target_properties(${REALM_LIBRARY} PROPERTIES IMPORTED_LOCATION ${LEGION_LIB_DIR}/librealm${LIBEXT})
	
		list(APPEND FLEXFLOW_INCLUDE_DIRS 
			${LEGION_INCLUDE_DIR} 
			${LEGION_INCLUDE_DIR}/hip_cuda_compat 
			${LEGION_INCLUDE_DIR}/legion 
			${LEGION_INCLUDE_DIR}/mappers 
			${LEGION_INCLUDE_DIR}/mathtypes 
			${LEGION_INCLUDE_DIR}/realm
		)
		
		install(DIRECTORY ${LEGION_SHARE_DIR} DESTINATION share)
		install(DIRECTORY ${LEGION_BIN_DIR} DESTINATION bin)
		install(DIRECTORY ${LEGION_LIB_DIR}/ DESTINATION lib)
		
	else()
		# Build Legion from source
		message(STATUS "Building Legion from source")
		if(FF_USE_PYTHON)
		  set(Legion_USE_Python ON CACHE BOOL "enable Legion_USE_Python")
		  set(Legion_BUILD_BINDINGS ON CACHE BOOL "build legion_python")
		endif()
		if("${FF_LEGION_NETWORKS}" STREQUAL "gasnet")
		  set(Legion_EMBED_GASNet ON CACHE BOOL "Use embed GASNet")
		  set(Legion_EMBED_GASNet_VERSION "GASNet-2022.3.0" CACHE STRING "GASNet version")
		  set(Legion_NETWORKS "gasnetex" CACHE STRING "GASNet conduit")
		  set(GASNet_CONDUIT ${FF_GASNET_CONDUIT})
		endif()
		message(STATUS "GASNET ROOT: $ENV{GASNet_ROOT_DIR}")
		set(Legion_MAX_DIM ${FF_MAX_DIM} CACHE STRING "Maximum number of dimensions")
		if (FF_GPU_BACKEND STREQUAL "cuda")
			set(Legion_USE_CUDA ON CACHE BOOL "enable Legion_USE_CUDA" FORCE)
			set(Legion_CUDA_ARCH ${FF_CUDA_ARCH} CACHE STRING "Legion CUDA ARCH" FORCE)
		elseif (FF_GPU_BACKEND STREQUAL "hip_cuda" OR FF_GPU_BACKEND STREQUAL "hip_rocm")
			set(Legion_USE_HIP ON CACHE BOOL "enable Legion_USE_HIP" FORCE)
			if (FF_GPU_BACKEND STREQUAL "hip_cuda")
				set(Legion_HIP_TARGET "CUDA" CACHE STRING "Legion_HIP_TARGET CUDA" FORCE)
				set(Legion_CUDA_ARCH ${FF_CUDA_ARCH} CACHE STRING "Legion CUDA ARCH" FORCE)
			elseif(FF_GPU_BACKEND STREQUAL "hip_rocm")
				set(Legion_HIP_TARGET "ROCM" CACHE STRING "Legion HIP_TARGET ROCM" FORCE)
				set(Legion_HIP_ARCH ${FF_HIP_ARCH} CACHE STRING "Legion HIP ARCH" FORCE)
				message(STATUS "Legion_HIP_ARCH: ${Legion_HIP_ARCH}")
			endif()
		endif()
		set(Legion_REDOP_COMPLEX OFF CACHE BOOL "disable complex")
		add_subdirectory(deps/legion)
		set(LEGION_LIBRARY Legion)
    
		set(LEGION_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/deps/legion/runtime)
		set(LEGION_DEF_DIR ${CMAKE_BINARY_DIR}/deps/legion/runtime)
	endif()
endif()
