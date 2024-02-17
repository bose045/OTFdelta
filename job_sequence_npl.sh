#!/bin/bash

# Submit the second script with a dependency on the first
jobID00 = $(sbatch --parsable -p npl-2024  run_autolearn_0_0.sh) ## initial folder setup
iter=0
jobID01=$(sbatch --parsable --dependency=afterany:$jobID00 --array=0-239 -p npl-2024 job_array_nnmd.sh $iter) ## 240 NNMD jobs
jobID02=$(sbatch --parsable --dependency=afterany:$jobID01 --array=0-7 -p npl-2024 job_modev.sh $iter) ## model deviation and copy to AIMD
iter = 1
jobID03 = $(sbatch --parsable --dependendency=afterany:$jobID02 -p npl-2024  run_autolearn_i_0.sh $iter) ## initial folder setup

#sbatch --array=1-$(wc -l < valid_run_dirs.txt) ../../dcs_array_aimd.sh
#sbatch --parsable --dependency=afterany:$jobID02 --cluster=dcs dcs_array_aimd.sh $iter
#jobID03=$(sbatch --parsable --dependency=afterany:$jobID02 -p npl-2024 catcandidates.sh $iter) ## concatenate candidates
#jobID04=$(sbatch --parsable --dependency=afterany:$jobID03 --array=0-2 -p npl-2024 train_job.sh $iter) ## train MACE with 3 seeds


