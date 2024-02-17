#!/bin/bash
#SBATCH -J NNmd
#SBATCH -p npl-2024
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --gres=gpu:6
#SBATCH -o jobfile.%j
#SBATCH --time=00:01:00

cd ./AllSys
cat AllSys_* > AllSys.xyz
