#!/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=test_job_%j.out
#SBATCH --time=00:10:00
#SBATCH --ntasks=1
#SBATCH --mem=1M

python autolearn_i_1.py $1> output.log 2> error.log
