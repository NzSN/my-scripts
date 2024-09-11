#!/usr/bin/bash

set -euo pipefail

THREADS="$(($(nproc --all) - 1))"

mkdir -p build_compiler-rt
mkdir -p build_runtimes

LLVM_PATH="$1"
INSTALL_PATH="$2"
TOOLCHAIN_DIR="$3"
SYSROOT_DIR="$TOOLCHAIN_DIR/loongarch64-linux-gnu/sysroot"
LA_FLAGS="-B$TOOLCHAIN_DIR/loongarch64-linux-gnu -mcmodel=large"

pushd "build_compiler-rt" || return

cmake                                                                     \
      -DCMAKE_BUILD_TYPE=Release                                          \
      -G "Unix Makefiles"                                                 \
      _DCMAKE_INSTALL_PREFIX="$INSTALL_PATH"                              \
      -DCMAKE_C_FLAGS="$LA_FLAGS"                                         \
      -DCMAKE_CXX_FLAGS="$LA_FLAGS"                                       \
      -DCMAKE_C_COMPILER="$TOOLCHAIN_DIR/bin/loongarch64-linux-gnu-gcc"   \
      -DCMAKE_CXX_COMPILER="$TOOLCHAIN_DIR/bin/loongarch64-linux-gnu-g++" \
      -DCMAKE_AR="$TOOLCHAIN/bin/loongarch64-linux-gnu-ar"                \
      -DCMAKE_NM="$TOOLCHAIN/bin/loongarch64-linux-gnu-nm"                \
      -DCMAKE_RANLIB="$TOOLCHAIN/bin/loongarch64-linux-gnu-ranlib"        \
      -DCMAKE_OBJCOPY="$TOOLCHAIN/bin/loongarch64-linux-gnu-objcopy"      \
      -DCOMPILER_RT_BUILD_BUILTINS=ON                                     \
      -DCOMPILER_RT_BUILD_LIBFUZZER=OFF                                   \
      -DCOMPILER_RT_BUILD_MEMPROF=ON                                      \
      -DCOMPILER_RT_BUILD_PROFILE=ON                                      \
      -DCOMPILER_RT_BUILD_SANITIZERS=ON                                   \
      -DCOMPILER_RT_BUILD_XRAY=ON                                         \
      -DCOMPILER_RT_DEFAULT_TARGET_ONLY=ON                                \
      -DCMAKE_C_COMPILER_TARGET="loongarch64-unknown-linux-gnu"           \
      -DCMAKE_ASM_COMPILER_TARGET="loongarch64-unknown-linux-gnu"         \
      -DCMAKE_SYSROOT="$SYSROOT_DIR"                                      \
      $LLVM_PATH/compiler-rt
make -j$THREADS
make install

exit 0
~
