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

iter=$(printf "%04d" $1)
output_dir="${iter}"
cd "$output_dir" || exit
curdir=$(pwd)
echo "Current directory: $curdir"

cp -r ./maceTrainPotential/* ../latestModel/
