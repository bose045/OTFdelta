#!/bin/bash
ssh -t "dcsfen01"<<EOF
target_directory=$1
#cd "$target_directory"
#echo "The current directory is: $(pwd)"
#cd AIMD

echo "Changing to directory: \$target_directory"
cd "\$target_directory" || { echo "Failed to change to directory \$target_directory"; exit 1; }
echo "The current directory is: \$(pwd)"
ls .
cd ./AIMD || { echo "AIMD directory not found in \$(pwd)"; exit 1; }
ls .
#echo "The current directory is: \$(pwd)"
ls .
current_directory=$(pwd)
echo "The current directory is: $current_directory"

for sys in */; do
    echo $sys
    cd $current_directory/$sys  || { echo "Failed to change to directory $sys"; continue; }
    echo "Thei current directory is: \$(pwd)"
    sysNum=$(echo "$sys" | sed 's/\///g')  # remove the / from the folder name

    # if not empty launch AIMD jobs
    if    ls -A1q . | grep -q .
    then

        for runFol in */; do
            # for runFol in run0002_0000_0000 run0002_0000_0001; do
            current_directory=$(pwd)
            cd $current_directory/$runFol
            echo "Theo current directory is: \$(pwd)"
            runNum=$(echo "$runFol" | sed 's/\///g')  # remove the / from the folder name
            cp ../../../../pybash/md.in .
            sbatch ../../../../pybash/jdftx-gpu.job $sysNum $runNum 
            cd ..
        done      

    else  
        echo empty - no runs in $sys
        # add the done flag here to just skip it 
        touch doneAIMDflag
    fi



    # sbatch ../../../../singleMultiGPUoneNode.job $sysNum
    # OLD bash ../../../../singleMultiGPUoneNode.job $sysNum
    cd ..
done
EOF
# ----moving below to next script in case job didn't finish and connection lost --- 
# for sys in */; do
#     cd $sys


#     # echo 'Waiting for doneAIMDflag'
#     # while [ ! -f doneAIMDflag ]
#     # do
#     #     sleep 2 # or less like 0.2
#     # done
#     # rm doneAIMDflag

#     # if not empty check for complete
#     if    ls -A1q . | grep -q .
#     then

#         # echo 'Waiting for squeue to clear completely from job'
#         while [ ! -f doneAIMDflag ]
#         do
#             # only jobid output if complete
#             if [ "$(squeue -u kamron -n singleMultiGPUoneNode.job -o %A)" = "JOBID" ]; then
#                 echo DONE $sys
#                 touch doneAIMDflag
#             fi 
#             sleep 2 # or less like 0.2
#         done
#         rm doneAIMDflag

#         # copy out 
#         for runFol in */; do
#             cd $runFol
#             cp *.jdftxout ../../../../DpmdTrainPotential/train/
#             cd ..
#         done    

#     fi

#     cd ..
# done

