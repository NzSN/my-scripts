#!/usr/bin/bash

BUILDER_PATH=bin/builder
BUILDERS=(
  "chromium" 
  "electron" 
  "llvm" 
  "rust"
)

BUILDER_SCRIPTS=""
for builder in "${BUILDERS[@]}"; do
  if [ "$BUILDER_SCRIPTS" == "" ]; then
    BUILDER_SCRIPTS="$BUILDER_PATH/$builder/build_${builder}.py"
  else
    BUILDER_SCRIPTS="$BUILDER_SCRIPTS:$BUILDER_PATH/$builder/build_${builder}.py"
  fi
done

BINS=$BUILDER_SCRIPTS:bin/builder/node/build_node_ffi_napi.py:bin/builder/builder.py
