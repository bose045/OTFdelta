#!/bin/bash

#SBATCH -J NNmd
#SBATCH -p npl-2024
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --gres=gpu:6
#SBATCH -o jobfile.%j
#SBATCH --time=00:02:00

if [ -z "$1" ]; then
    echo "Usage: $0 <number>"
    exit 1
fi

> candidates.xyz

iter=$(printf "%04d" $1)
for i in {0..7}; do 
    cat $iter/NNmd/sys${i}/candidates.xyz >> candidates.xyz
done

cp AllSys.xyz AllSysLast.xyz
cat AllSys.xyz candidates.xyz> AllSys.xyz
rm candidates.xyz