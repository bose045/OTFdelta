#!/bin/bash

# process jdftxouts to DeePMD input
cd DpmdTrainPotential
# parse jdftxout with custom dpdata
# export pathToJdftxParser=/global/homes/k/kamron/dpdatajdftx/VariableParseAIMDtoDPMD.py
# python $pathToJdftxParser 10 > conversionInfo$1
python /global/homes/k/kamron/dpdatajdftx/VariableParseAIMDtoDPMD.py 10 > conversionInfo$1

for dir in seed*/; do
  cd $dir

  # HACK:
  # cp ../../inputMini.json input.json
  cp ../../inputInitial.json input.json

  cd ..
done


# lauch training
sbatch ../multiTrainInit.job

# wait until done training
echo 'Waiting for doneTrainingflag'
while [ ! -f doneTrainingFlag ]
do
  sleep 2 # or less like 0.2
done

rm doneTrainingFlag


for dir in seed*/; do
  cd $dir
  # save lcurve for each iteration 
  mv lcurve.out lcurve${1}.out
  # seedNum = $(echo "$dir" | sed 's/\///g')
  # remove last model if there is one
  # rm frozenModel*
  #freeze model
  dp freeze -o frozenModel.pb
  # store a version of each model for now
  cp frozenModel.pb frozenModel${1}.pb
  cd ..
done



