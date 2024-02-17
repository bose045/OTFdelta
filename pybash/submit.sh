#!/bin/bash -l
#SBATCH -J DeepPot_training
#SBATCH -p npl
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -i input.json
#SBATCH --gres=gpu:6
#SBATCH -o jobfile.%j
#SBATCH -e deepMDtrain.%j

#---------Modules to load-----------------------------------------------------------------------------------------
module load gcc/8.4.0/1 cuda/10.2 cuda/11.1 openmpi/4.0.3/1

source ~/scratch-shared/npl_miniconda/etc/profile.d/conda.sh

conda activate deepmd_gpu

#---------Job description

export OMP_NUM_THREADS=40 # Hyperthreading

# Restart if there are restart files else start the training:
if ls model.ckpt.* 1> /dev/null 2>&1; then
# Restart job
srun dp train --restart model.ckpt input.json # Restart training
else
# Initial
srun dp train input.json # Fresh training
fi
