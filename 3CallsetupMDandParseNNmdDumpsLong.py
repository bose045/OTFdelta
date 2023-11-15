import numpy as np
import sys
import gzip
import os
import glob
import random
import time

# setup and run lammps for each system
# repeat so many times before training based on different seeds
totalLammpsCycles = 30
LOlammpsNum = 0 # set to ncycle value from last 

if len(sys.argv) < 2:
    print('Usage: 3Call...py <current iteration folder index number>')
    exit(1)

folderIter = sys.argv[1]  # training iteration number in 0000 form 

# In this range of lo and hi * avg of max values items are extracted 
model_devi_f_trust_lo = 1. # was 0.05 and 0.15
model_devi_f_trust_hi = 5.
sampleFreq = 10  # if lammps out_freq 10, timestep 5fs, then sampleFreq 100 is checking configs every 50fs
# sampleFreq must be >=lammps out_freq and a multiplier of it (e.g., 10,20,100,1000)

# freeze new model before running MD
os.system(f'bash ../../1aFreezeModel.sh {folderIter}')

os.chdir('NNmd')

for nCycle in range(totalLammpsCycles):
    # HACK comment below to bypass MD sims
    print('nCycle=',nCycle)
    os.system('bash ../../../3setupMD.sh')
    
    # parse output for high error configs
    # pull out configs to ConfigsForAIMD folder for training in next iteration
    systems = sorted(glob.glob('./*/'))
    print(systems)
    for sysNum, sysFolder in enumerate(systems):

        os.chdir(sysFolder)
        # TODO Add a check if there are no runs and then break

        #Usage: lammpsToJDFTx.py <dumpFile> <outPrefix> <current iteration folder index number> <lammps cycle number> <system number> <filename for model deviation file> <model_devi_f_trust_lo> <model_devi_f_trust_hi> <sampleFreq>
        os.system(f'python ../../../../lammpsToJDFTx.py output.dump md {folderIter} {nCycle+LOlammpsNum} {sysNum} md.out {model_devi_f_trust_lo} {model_devi_f_trust_hi} {sampleFreq} > SnapsForAIMD{folderIter}_{nCycle+LOlammpsNum}_{sysNum}')
        # python ../../../../lammpsToJDFTx.py output.dump md  {sysNum} md.out {model_devi_f_trust_lo} {model_devi_f_trust_hi} {sampleFreq} > {sysNum}SnapsForAIMD
        os.system(f'cp output.dump output{folderIter}_{nCycle+LOlammpsNum}_{sysNum}.dump')
        os.system(f'cp md.out md{folderIter}_{nCycle+LOlammpsNum}_{sysNum}.out')
        # save and rename hist and max error plots
        os.system(f'mv hist.pdf hist{folderIter}_{nCycle+LOlammpsNum}_{sysNum}.pdf')
        os.system(f'mv MaxOverTime.pdf MaxOverTime{folderIter}_{nCycle+LOlammpsNum}_{sysNum}.pdf')
        os.chdir('..')

    