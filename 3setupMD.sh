#!/bin/bash

sbatch ../../../3setupMD.job
# bash ../../../3setupMD.job  # for quick check


# wait until done 
echo 'Waiting for doneMDflag'
while [ ! -f doneMDflag ]
do
  sleep 2 # or less like 0.2
done
echo 'Detected doneMDflag'
rm doneMDflag