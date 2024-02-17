#!/bin/bash

# Set the initial current directory path
target_directory=$1
echo "Changing to directory: $target_directory"
cd "$target_directory" || { echo "Failed to change to directory $target_directory"; exit 1; }
echo "The current directory is: $(pwd)"

current_directory=$(pwd)

for sys in */; do
    if [ -d "$sys" ]; then  # Check if $sys is indeed a directory
        echo "Found system directory: $sys"
        sys_path="${current_directory}/${sys}"
        echo "Full system path: $sys_path"

        # Check if the system directory is not empty
        if [ -n "$(ls -A "$sys_path")" ]; then
            for runFol in "${sys_path}"*/; do
                if [ -d "$runFol" ]; then  # Check if $runFol is a directory
                    run_path="$runFol"
                    echo "Run folder path: $run_path"

                    # Copy the file to the run folder path
                    cp "${current_directory}/../../../../pybash/md.in" "$run_path"
                    echo "Copied md.in to $run_path"

                    # Launch the job
                    sbatch "${current_directory}/../../../../pybash/jdftx-gpu.job" "$sysNum" "$runNum"
                    echo "Launched job in $run_path"
                fi
            done
        else
            echo "Empty - no runs in $sys"
            touch "${sys_path}doneAIMDflag"
            echo "Marked $sys as done"
        fi
    fi
done

