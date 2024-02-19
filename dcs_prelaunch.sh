#!/bin/bash
iter=$1
folderIter=$(printf "%04d" $iter)
cd ./${folderIter}/AIMD
find . -type d -links 2 | sed 's|^\./||' | sort > valid_run_dirs.txt
