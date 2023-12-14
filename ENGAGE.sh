#!/usr/bin/env sh

# --- CLI (common) ---
cd common
mkdir --parents src/common
git add src
git mv *.py src/common/.
cd ..

# --- GUI (qt) ---
cd qt
mkdir --parents src/qt
git add src
git mv *.py src/qt/.
cd ..

# --- clean make file system ---
git rm common/configure
git rm qt/configure
