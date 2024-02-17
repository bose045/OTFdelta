#!/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=test_job_%j.out
#SBATCH --time=00:00:30
#SBATCH --ntasks=1
#SBATCH --mem=1M

# The script does practically nothing except printing a message
echo "Test job running at $(date)">echoline.txt

