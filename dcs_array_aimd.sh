#!/bin/bash
#SBATCH -N 1 -n 1 -t 1 --gres=gpu:1 -o md.o%j
# SLURM array job script

iter=$1
folderIter=$(printf "%04d" $iter)
cd ./${folderIter}/AIMD

# Read the run directory from the file based on SLURM_ARRAY_TASK_ID
run_dir=$(sed -n "${SLURM_ARRAY_TASK_ID}p" valid_run_dirs.txt)
sysNum=$(echo "$run_dir" | cut -d'/' -f1)
runFol=$(echo "$run_dir" | cut -d'/' -f2)
numericPart=${sysNum#sys}

# Determine job file based on sysNum
if [[ $numericPart -ge 0 ]] && [[ $sysNum -le 4 ]]; then
    jobFile="../../../../pybash/jdftx-gpu.job"
elif [[ $numericPart -ge 5 ]] && [[ $sysNum -le 7 ]]; then
    jobFile="../../../../pybash/jdftx-gpu-2.job"
else
    jobFile="../../../../pybash/jdftx-gpu.job"
fi

#jobFile="../../../../pybash/nothing.sh"

cd $sysNum/$runFol
cp ../../../../pybash/md.in .
sbatch $jobFile $sysNum $(echo "$runFol" | sed 's/\///g')
#touch mdlaunch_$sysNum_$runFol
cd ../..

