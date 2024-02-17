#!/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=test_job_%j.out
#SBATCH --time=00:01:00
#SBATCH --ntasks=1
#SBATCH --mem=1M

python autolearn_0_0.py > output_00.log 2> error.log
