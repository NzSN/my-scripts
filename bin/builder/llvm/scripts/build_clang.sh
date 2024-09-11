#!/usr/bin/bash

set -euo pipefail

THREADS="$(($(nproc --all) - 1))"

LLVM_PATH="$1"
INSTALL_PATH="$2"
BUILD_DIR="$3"

mkdir -p "$BUILD_DIR"

pushd "$BUILD_DIR" || return

cmake                                       \
     -DLLVM_ENABLE_PROJECTS="clang;lld"     \
     -DCMAKE_BUILD_TYPE=Release             \
     -DLLVM_ENABLE_RUNTIMES="compiler-rt"   \
     -DLLVM_INSTALL_UTILS=ON                \
     -DCMAKE_INSTALL_PREFIX="$INSTALL_PATH" \
     -DLLVM_ENABLE_OCAMLDOC=OFF             \
     -DLLVM_ENABLE_BINDINGS=OFF             \
     -DLLVM_BUILD_LLVM_DYLIB=ON             \
     -DLLVM_LINK_LLVM_DYLIB=ON              \
     -DCOMPILER_RT_BUILD_LIBFUZZER=OFF      \
     -DLLVM_ENABLE_FFI=ON                   \
     -DLLVM_ENABLE_RTTI=ON                  \
     -DLLVM_ENABLE_ASSERTIONS=OFF           \
     -DLLVM_APPEND_VC_REV=OFF               \
     -G "Unix Makefiles"                    \
      $LLVM_PATH/llvm
make -j$THREADS
make install

exit 0
