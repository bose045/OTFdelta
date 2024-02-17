#!/bin/bash

# process jdftxouts to DeePMD input
cd DpmdTrainPotential
# parse jdftxout with custom dpdata
# export pathToJdftxParser=/global/homes/k/kamron/dpdatajdftx/VariableParseAIMDtoDPMD.py
# python $pathToJdftxParser 10 > conversionInfo$1
#python /global/homes/k/kamron/dpdatajdftx/VariableParseAIMDtoDPMD.py 10 > conversionInfo$1
source ~/scratch-shared/npl_miniconda/etc/profile.d/conda.sh
conda activate deepmd
python /gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/OTFdelta1/pybash/VariableParseAIMDtoDPMD.py 1 False True > conversionInfo${1}
conda deactivate
for dir in seed*/; do
  cd $dir

  # HACK:
  # cp ../../inputMini.json input.json
  cp ../../../pybash/inputInitial.json input.json
#  sbatch -t 3 ../../../pybash/submit.sh 
  cd ..
done


# lauch training
#sbatch ../multiTrainInit.job
#sbatch -t 3 ../../pybash/submit.sh
source ~/scratch-shared/npl_miniconda/etc/profile.d/conda.sh
conda activate deepmd_gpu
sbatch -t 360  /gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/OTFdelta1/pybash/multitrain2.job > logmultijob

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
  dp compress -i frozenModel.pb -o frozen-compress.pb
  # store a version of each model for now
  cp frozenModel.pb frozenModel${1}.pb
  cp frozenModel.pb frozen-compress${1}.pb
  cd ..
done
conda deactivate

