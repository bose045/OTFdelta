#!/bin/bash

# Iterate over all .data files
for file in *.data; do
    # Extract the base name of the file without the .data extension
    base_name=$(basename "$file" .data)

    # Use awk to split the file content
    awk -v base="$base_name" '
    BEGIN {
        printStart = 1;
        printEnd = 0;
    }
    /Atoms # full/ {
        printStart = 0;
    }
    /Masses/ {
        printStart = 0;
        printEnd = 1;
    }
    {
        if (printStart) print > (base "_START.data");
        if (printEnd) print > (base "_END.data");
    }' "$file"
done

