#!/bin/bash

#SBATCH -J NNmd
#SBATCH -p npl-2024
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --gres=gpu:6
#SBATCH -o jobfile.%j
#SBATCH --time=01:00:00

if [ -z "$1" ]; then
    echo "Usage: $0 <number>"
    exit 1
fi

iter=$(printf "%04d" $1)
id=$SLURM_ARRAY_TASK_ID
quot=$((id/8))
sysNum=$((id%8)) 

cd ${iter}/NNmd/sys${sysNum}

#touch run${quot}_sys${sysNum}

python ../../../pybash/MDdelta.py "sys${sysNum}_init.data" ${sysNum} ${quot} > outputfile

