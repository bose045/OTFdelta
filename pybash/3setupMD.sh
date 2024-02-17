#!/bin/bash

sbatch  -t 1:20:00 /gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/OTFdelta1/pybash/submit_run_tmgn.sh
# bash ../../../3setupMD.job  # for quick check
#sbatch --gres=gpu:6 -n 16 -N 1 -t 100 --job-name=alcutrest ./submit_run.sh

# wait until done 
echo 'Waiting for doneMDflag'
while [ ! -f doneMDflag ]
do
  sleep 2 # or less like 0.2
done
echo 'Detected doneMDflag'
rm doneMDflag
