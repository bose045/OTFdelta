#!/bin/bash
#SBATCH -N 1 -n 1 -t 1 --gres=gpu:1 -o md.o%j
# Script to generate a list of valid run directories
output_file="valid_run_dirs.txt"
rm -f $output_file  # Remove the file if it exists

for sys in sys*/; do
    cd $sys
    sysNum=$(echo "$sys" | sed 's/\///g')  # Remove the / from the folder name

    # Check if sys folder is not empty
    if ls -A1q . | grep -q .; then
        for runFol in run*/; do
            if [ "$(ls -A $runFol)" ]; then
                echo "$sysNum/$runFol" >> ../$output_file
            fi
        done
    else
        echo "Empty - no runs in $sys"
    fi

    cd ..
done

