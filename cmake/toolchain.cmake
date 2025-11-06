
set(SDK_PATH "/.sdk")
set(COMPILER_PATH "${SDK_PATH}/compiler/bin")

set(CMAKE_SYSROOT "${SDK_PATH}/${TARGET_ARCH}")
set(CMAKE_C_COMPILER "${COMPILER_PATH}/clang")
set(CMAKE_CXX_COMPILER "${COMPILER_PATH}/clang++")
set(CMAKE_AR "${COMPILER_PATH}/llvm-ar")
set(CMAKE_RANLIB "${COMPILER_PATH}/llvm-ranlib")
set(CMAKE_NM "${COMPILER_PATH}/llvm-nm")
set(CMAKE_ASM_COMPILER "${COMPILER_PATH}/clang")

set(COMMON_CLANG_FLAGS "--target=${TARGET_ARCH} --sysroot=${CMAKE_SYSROOT} -rtlib=compiler-rt -I${CMAKE_SYSROOT}/include/c++/v1")
set(CMAKE_LIBRARY_PATH "${CMAKE_SYSROOT}/lib")

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${COMMON_CLANG_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${COMMON_CLANG_FLAGS} -stdlib=libc++ -fno-exceptions -fno-rtti")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fuse-ld=lld -Wl,-dynamic-linker,${CMAKE_SYSROOT}/lib/libc.so")
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -fuse-ld=lld")