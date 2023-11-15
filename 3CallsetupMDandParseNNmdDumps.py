import numpy as np
import sys
import gzip
import os
import glob
import random
import time

# setup and run lammps for each system
# repeat so many times before training based on different seeds
# python ../../3CallsetupMDandParseNNmdDumps.py 0006 | tee ../iterOut6c
totalLammpsCycles = 30  # run up to this total MDs
LOlammpsNum = 0 # set to ncycle value from last 
maxTotalCandidates = 300 # once total candidates across systems gathered is greater than this stop
maxPerMDCandidates = 30 # limit total candidates per MD run


if len(sys.argv) < 2:
    print('Usage: 3Call...py <current iteration folder index number>')
    exit(1)

folderIter = sys.argv[1]  # training iteration number in 0000 form 

# In this range of lo and hi * avg of max values items are extracted 
model_devi_f_trust_lo = 0.05
model_devi_f_trust_hi = 0.15
sampleFreq = 100  # was 10 for iter 0-5
# if lammps out_freq 10, timestep 5fs, then sampleFreq 100 is checking configs every 50fs
# sampleFreq must be >=lammps out_freq and a multiplier of it (e.g., 10,20,100,1000)


os.chdir('NNmd')

for nCycle in range(totalLammpsCycles):
    # HACK comment below to bypass MD sims
    print('nCycle=',nCycle)
    os.system('bash ../../../3setupMD.sh')
    
    # parse output for high error configs
    # pull out configs to ConfigsForAIMD folder for training in next iteration
    systems = sorted(glob.glob('./*/'))
    print(systems)
    totalCandidates = 0  # initialize tracking variable before counting all up

    for sysNum, sysFolder in enumerate(systems):

        os.chdir(sysFolder)
        # read in existing number of candidates across each sys and sum them up
        
        for fname in sorted(glob.glob('Snaps*')):
            
            try:
                with open(fname,'r') as f:
                    for line in f:
                        if line.startswith("Number of possible candidates"):
                            # print(line.split())
                            # sys.exit(1)
                            candidateWithMin = min(maxPerMDCandidates, int(line.split()[4])) # value should match lammps # TODO pass that variable in
                            totalCandidates += candidateWithMin
                print('fname', fname,' totalCandidates=',totalCandidates)
            except:
                print('file cant open')

        

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

    # if enough candidates collected stop running MD
    if totalCandidates > maxTotalCandidates:
        break