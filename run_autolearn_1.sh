#!/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=test_job_%j.out
#SBATCH --time=00:01:00
#SBATCH --ntasks=1
#SBATCH --mem=1M

# The script does practically nothing except printing a message

echo $1

python autolearn_1.py $1  > output.log 2> error.log
