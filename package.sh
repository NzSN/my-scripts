#!/usr/bin/bash

BUILDER_PATH=bin/builder
BUILDERS=(
  "chromium" 
  "electron" 
  "llvm" 
  "rust"
)

BUILDERS=""
for builder in "${BUILDERS[@]}"; do
  if [ "$BUILDERS" == "" ]; then
    BUILDERS="$BUILDER_PATH/$builder/build_${builder}"
  else
    BUILDERS="$BUILDERS:$BUILDER_PATH/$builder/build_${builder}"
  fi
done
echo $BUILDERS

 BINS=bin/builder
