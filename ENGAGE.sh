#!/usr/bin/env sh

# --- CLI (common) ---
cd common
mkdir --parents src/common
git add src
git mv *.py src/common/.

