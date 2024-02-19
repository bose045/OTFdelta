#!/bin/bash
iter = $1

#folderIter=$(printf "%04d" $iter)
#cd /gpfs/u/home/TMGN/TMGNprbs/scratch-shared/PolyGroup/maceOTFdelta/Autolearn/$folderIter
#find . -type d -links 2 | sed 's|^\./||' | sort > valid_run_dirs.txt
#sbatch --parsable --array=1-$(wc -l < valid_run_dirs.txt)

# After dcs jobs are completed
jobID00=$(sbatch --parsable -p npl-2024  run_autolearn_i_1.sh $iter) ## get delta (JDFTX-->xyz every single frame [dpdatajdftx])
jobID000=$(sbatch --parsable --dependency=afterany:$jobID00 --array=0-7 -p npl-2024 job_toXYZ.sh $iter)
jobID0000=$(sbatch --parsable --dependency=afterany:$jobID000 -p npl-2024 job_catXYZ.sh $iter)
jobID00000=$(sbatch --parsable --dependency=afterany:$jobID0000 -p npl-2024 job_catAllXYZ.sh $iter)

jobID0T=$(sbatch --parsable --dependency=afterany:$jobID00000 --array=0-2 -p npl-2024 train.job $iter) ## train
jobID001=$(sbatch --parsable --dependency=afterany:$jobID0T -p npl-2024 run_autolearn_i_2.sh $iter) 
jobID002=$(sbatch --parsable --dependency=afterany:$jobID001 -p npl-2024 copy_latest_model.sh $iter) ## copy latest model
jobID01=$(sbatch --parsable --dependency=afterany:$jobID002 --array=0-239 -p npl-2024 job_array_nnmd.sh $iter) ## 240 NNMD jobs
jobID02=$(sbatch --parsable --dependency=afterany:$jobID01 --array=0-7 -p npl-2024 job_modev.sh $iter) ## model deviation and copy to AIMD

#iter = 2
#jobID03 = $(sbatch --parsable --dependendency=afterany:$jobID02 -p npl-2024  run_autolearn_i_0.sh $iter) ## i
### Launch AIMD jobs
### After dcs jobs are completed
#jobID00=$(sbatch --parsable -p npl-2024  run_autolearn_i_1.sh $iter) ## get delta (JDFTX-->xyz every single frame [dpdatajdftx])
#jobID000=$(sbatch --parsable --dependency=afterany:$jobID00 --array=0-7 -p npl-2024 job_toXYZ.sh $iter)
#jobID0000=$(sbatch --parsable --dependency=afterany:$jobID000 -p npl-2024 job_catXYZ.sh $iter)
#jobID00000=$(sbatch --parsable --dependency=afterany:$jobID0000 -p npl-2024 job_catAllXYZ.sh $iter)

#jobID0T=$(sbatch --parsable --dependency=afterany:$jobID00000 --array=0-2 -p npl-2024 train.job $iter) ## train
#jobID001=$(sbatch --parsable --dependency=afterany:$jobID0T -p npl-2024 run_autolearn_i_2.sh $iter)
#jobID002=$(sbatch --parsable --dependency=afterany:$jobID001 -p npl-2024 copy_latest_model.sh $iter) ## copy latest model
#jobID01=$(sbatch --parsable --dependency=afterany:$jobID002 --array=0-239 -p npl-2024 job_array_nnmd.sh $iter) ## 240 NNMD jobs
#jobID02=$(sbatch --parsable --dependency=afterany:$jobID01 --array=0-7 -p npl-2024 job_modev.sh $iter) ## model deviation and copy to AIMD

