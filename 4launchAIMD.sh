#!/bin/bash

cd AIMD


for sys in */; do
    cd $sys
    sysNum=$(echo "$sys" | sed 's/\///g')  # remove the / from the folder name

    # if not empty launch AIMD jobs
    if    ls -A1q . | grep -q .
    then

        for runFol in */; do
            # for runFol in run0002_0000_0000 run0002_0000_0001; do
            cd $runFol
            runNum=$(echo "$runFol" | sed 's/\///g')  # remove the / from the folder name
            cp ../../../../md.in .
            sbatch ../../../../../singleMultiGPUoneNode.job $sysNum $runNum 
            cd ..
        done      

    else  
        echo empty - no runs in $sys
        # add the done flag here to just skip it 
        # touch doneAIMDflag  not needed since it would fill a dir and throw off TrainNew which checks for empty
    fi



    # sbatch ../../../../singleMultiGPUoneNode.job $sysNum
    # OLD bash ../../../../singleMultiGPUoneNode.job $sysNum
    cd ..
done

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

