# notes
# on PM conda activate deepmd3
# start in Autodelta folder
# run this with nohup python AutoLearn.py > out &

import numpy as np
import sys
import gzip
import os
import glob

print('latest change: ___')

pattern = '*.jdftxout'
# 0000 is the initial setup with initial each system folder

# ----------
# SETUP folder structure:
# os.chdir('AutoDelta')
os.getcwd()

# os.chdir('VaspDataGen')

# convert to poscar (for each type of system (# atoms, bond types))
# for pathAndFilename in sorted(glob.iglob(os.path.join(os.getcwd(), '*.jdftxout'))):
#     os.system(rf'python ../../jmd2allpos.py -f {pathAndFilename}')
# run each system type in initial LDFG (has config and vasp)
for pathAndFilename in sorted(glob.iglob(os.path.join(os.getcwd(), '*.vasp'))):
    os.system(rf'python /gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/LammpsDataFileGeneratorKF/LDFG.py {pathAndFilename}')

# sys.exit()


# os.chdir(r'../0000')
# os.system(r'mkdir -p Train/train')
# os.system(r'mkdir -p Delta/{sys1,sys2,sys3,sys4}')
# os.system(r'mkdir -p NNmd')
