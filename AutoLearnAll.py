# notes
# conda activate deepmd EAGLE
# conda activate deepmd2 PM 
# start in Autolearn folder

# on screen or tmux with python ../AutoLearnAll.py | tee iterOut7

import numpy as np
import sys
import gzip
import os
import glob
import random
import time

print('latest change: ___')
print('System with all atoms must be listed alphabetically first to preserve order (e.g., add a 0 to filename prefix).')
print('4 training seeds are used matching 4 gpus/node')

# start in base folder (e.g., AutolearnEx)

# os.system('bash ../0initFolderSetup.sh') HACK add back in
# be sure to have your AIMD initial runs included in train


# for trainIter in range(2):
for trainIter in [8]:
    folderIter = f'{trainIter:04d}'
    print(f'{folderIter}')
    os.mkdir(folderIter)

    if trainIter == 0:
        # AIMD data should already be loaded into train folder
        print('Initial Training')
        os.system(f'bash ../1TrainInitial.sh {folderIter}')  
        

    os.chdir(folderIter)
    os.system('bash ../../2folderSetup.sh')

    if trainIter > 0:
        # copy high config errors from last ConfigsForAIMD into AIMD folders for each
        print('Copy uncertain configs for AIMD')
        os.system(f'cp -r ../{(trainIter-1):04d}/ConfigsForAIMD/* AIMD/')
        # cp -r ../0000/ConfigsForAIMD/* AIMD/
        # copy in md.in to each run folder and run AIMD
        # and copy jdftxouts to DpmdTrainPotential/train folder
        print('Launch AIMD')
        os.system(f'bash ../../4launchAIMD.sh')
                
        # train new NNPs
        print('New NNP training')
        os.system(f'bash ../../1TrainNew.sh {folderIter}') 
        # os.system(f'bash ../1TrainInitial.sh {folderIter}')  
        # bash ../../1TrainNew.sh 0004
        
        # freeze new model before running MD
        print('Freezing model')
        os.system(f'bash ../../1aFreezeModel.sh {folderIter}')


    # run NNMD and parse dumps into AIMD input
    print('Setup MD and run then parse output')
    os.system(f'python ../../3CallsetupMDandParseNNmdDumps.py {folderIter}')
    
    # return to base folder (e.g., AutolearnEx)
    os.chdir('..')
