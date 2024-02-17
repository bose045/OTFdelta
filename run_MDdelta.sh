#!/bin/bash
#SBATCH --output=test_job_%j.out
#SBATCH --time=00:5:00
#SBATCH --ntasks=1
#SBATCH --gres=gpu:6
# The script does practically nothing except printing a message
FPath="/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/maceOTFdelta/Autolearni/pybash/"

python "$FPath/MDdelta.py" > output.log 2> error.log
