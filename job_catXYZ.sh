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

output_dir="${iter}/deltaProcess/"
cd $output_dir || exit
echo "current directory is $(pwd)"
find . -type f -name "iter_${iter}_sys*.xyz" -exec cat {} + > AllSys_${iter}.xyz
cp  AllSys_${iter}.xyz ../../AllSys/
#python ../../../pybash/jdftxoutToXYZstep1.py iter_${iter}_sys$id.xyz
