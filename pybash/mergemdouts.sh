#!/bin/bash

# Loop through each sys$j folder
for j in {0..7}; do
    folder_name="sys$j"
    merged_file="${folder_name}/merged_data.out"

    # Concatenate files while removing lines starting with '#'
    grep -vh '^#' "${folder_name}/md0000_"*"_${j}.out" > "$merged_file"
done

