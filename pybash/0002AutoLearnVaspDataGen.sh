#!/bin/bash

#source activate mace_env
source ~/scratch-shared/npl_miniconda/etc/profile.d/conda.sh
conda activate mace_env
cp ../pybash/config .
python ../pybash/AutoLearnVaspDataGen.py
conda deactivate
