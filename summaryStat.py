import numpy as np
import sys
import gzip
import os
import glob
import random
import time
import parsing_md_out_atomic as modev
import matplotlib.pyplot as plt

# setup and run lammps for each system
# repeat so many times before training based on different seeds
# python ../../3CallsetupMDandParseNNmdDumps.py 0006 | tee ../iterOut6c
# totalLammpsCycles = 30  # run up to this total MDs
# LOlammpsNum = 0 # set to ncycle value from last 
# maxTotalCandidates = 300 # once total candidates across systems gathered is greater than this stop
# maxPerMDCandidates = 30 # limit total candidates per MD run


# if len(sys.argv) < 2:
#     print('Usage: ...py <>')
#     exit(1)

# folderIter = sys.argv[1]  # training iteration number in 0000 form 

# In this range of lo and hi * avg of max values items are extracted 
model_devi_f_trust_lo = 0.0
model_devi_f_trust_hi = 0.5
sampleFreq = 10  # 10 to match and include all
# if lammps out_freq 10, timestep 5fs, then sampleFreq 100 is checking configs every 50fs
# sampleFreq must be >=lammps out_freq and a multiplier of it (e.g., 10,20,100,1000)

# start in Autolearn folder
systems = ['sys0','sys1','sys2'] # ['sys0'] # 
iters = [4,5,6]

meanAll = np.zeros((len(systems), len(iters))) 
stdAll = np.zeros((len(systems), len(iters))) 
MDruns = np.zeros((len(systems), len(iters))) 


for isys, sys in enumerate(systems):


    for iIter, iter in enumerate(iters):
        folderIter = f'{iter:04d}'
        os.chdir(folderIter)
        os.chdir('NNmd')
        os.chdir(sys)

        # totalCandidates = 0  # initialize tracking variable before counting all up
        candidatesAll = []

        for i,modev_fname in enumerate(sorted(glob.glob('md0*out'))):

            
            # parse output for high error configs
            # pull out configs to ConfigsForAIMD folder for training in next iteration
            # systems = sorted(glob.glob('./*/'))
            # print(systems)
            
            candidates = modev.get_possible_candidates(modev_fname, model_devi_f_trust_lo, model_devi_f_trust_hi,sampleFreq) 
            candidatesAll.append(len(candidates))
            # print(f'Md.out {i} Number of possible candidates: {len(candidates)}')
            # if i==2:
            #     break

        # print(f'Number over total: {totalCandidates/(i+1)}') # 0 based i
        print('MEAN', np.mean(candidatesAll))
        print('STD ERR', np.std(candidatesAll)/(i+1)) # i zero based so +1

        MDruns[isys,iIter] = i+1
        meanAll[isys,iIter] = np.mean(candidatesAll)
        stdAll[isys,iIter] = np.std(candidatesAll)/(i+1)

        os.chdir('../../../')



np.save('meanAll.npy',meanAll)
np.save('stdAll.npy',stdAll)
np.save('MDruns.npy',MDruns)

# plt.close('all')
plt.figure(figsize=(7,5), dpi=300)
for isys, sys in enumerate(systems):
    plt.plot(iters, meanAll[isys,:], label=sys, marker='o')
    plt.fill_between(iters, meanAll[isys,:]-stdAll[isys,:], meanAll[isys,:]+stdAll[isys,:],facecolor='r',alpha=0.5)

plt.xlabel("Iterations")
plt.ylabel(f"Mean of # frames < {model_devi_f_trust_hi} samplefreq of {sampleFreq} (5fs sampling)")   
plt.xticks(iters)
# plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1)) 
# plt.xlim((-0.5,0.5))
# plt.ylim((0.,4))
plt.legend()
plt.savefig('summary.pdf')



# os.chdir('NNmd')







