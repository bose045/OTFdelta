#!/bin/bash

#!/bin/bash

# Create the datafiles directory
mkdir -p ./datafiles

# Loop through each sample_i directory
for i in {0..7}; do
    # Process neat_epoxy_before_deform
    if [ -d "./sys$i" ]; then
        mkdir -p "./datafiles/sys$i"
        find "sys$i" -type f -name "hist*" -exec cp {} "./datafiles/sys$i/" \;
    fi
done

# Compress the datafiles folder
tar -czvf datafiles.tar.gz ./datafiles

