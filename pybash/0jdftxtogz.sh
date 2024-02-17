#!/bin/bash
for file in *.jdftxout; do gzip -c "$file" > "$file.gz"; done
