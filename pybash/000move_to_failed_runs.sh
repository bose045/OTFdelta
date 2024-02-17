#!/bin/bash/
mkdir failed_runs
find . -type f -name '*.jdftxout' -size -150k -exec mv {} ./failed_runs \;
