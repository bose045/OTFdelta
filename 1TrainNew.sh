#!/bin/bash

# copy in AIMD files 

cd AIMD

for sys in */; do
    cd $sys

    # if not empty check for complete
    if    ls -A1q . | grep -q .
    then

        # echo 'Waiting for squeue to clear completely from job'
        while [ ! -f doneAIMDflag ]
        do
            # only jobid output if complete
            if [ "$(squeue -u kamron -n singleMultiGPUoneNode.job -o %A)" = "JOBID" ]; then
                echo DONE $sys
                touch doneAIMDflag
            fi 
            sleep 2 # or less like 0.2
        done
        rm doneAIMDflag

        # copy out 
        
        for runFol in */; do
            cd $runFol
            cp *.jdftxout ../../../../DpmdTrainPotential/train/
            cd ..
        done    

    fi

    cd ..
done


# process jdftxouts to DeePMD input
cd ../../DpmdTrainPotential
# parse jdftxout with custom dpdata
# export pathToJdftxParser=/global/homes/k/kamron/dpdatajdftx/VariableParseAIMDtoDPMD.py
# python $pathToJdftxParser 10 > conversionInfo$1
python /global/homes/k/kamron/dpdatajdftx/VariableParseAIMDtoDPMD.py 10 > conversionInfo$1

for dir in seed*/; do
  cd $dir
  
  # HACK:
  # cp ../../inputMini.json input.json
  # cp ../../inputNewRuns.json input.json  # not using restart from pb since it requires davg zero term
  cp ../../inputInitial.json input.json

  cd ..
done


# launch training
# sbatch ../multiTrainNew.job # not using restart from pb 
# remove done flag in case it was there before
rm doneTrainingFlag
sbatch ../multiTrainInit.job

# JOBID=$(sbatch ../multiTrainInit.job)
# JOBID=$(echo $JOBID | sed 's/Submitted batch job //g')
# echo $JOBID


# wait until done training
echo 'Waiting for doneTrainingflag'
while [ ! -f doneTrainingFlag ]
do
  sleep 2 # or less like 0.2
done
echo 'Detected doneTrainingflag!'
rm doneTrainingFlag

# move this in next script since it often doesn't get here

# for dir in seed*/; do
#   cd $dir
#   # save lcurve for each iteration 
#   mv lcurve.out lcurve${1}.out
#   # seedNum = $(echo "$dir" | sed 's/\///g')
#   # remove last model if there
#   # rm frozenModel*
#   #freeze model
#   dp freeze -o frozenModel.pb
#   # store a version of each model for now
#   cp frozenModel.pb frozenModel${1}.pb
#   cd ..
# done

# launch 
# JOBID=$(sbatch -d afterany:$JOBID /global/homes/k/kamron/Scratch/DFT/sequMultiSingleDir.job)
# JOBID=$(echo $JOBID | sed 's/Submitted batch job //g')
# echo $JOBID
