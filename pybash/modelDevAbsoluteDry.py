from ase import units
#from ase.md.langevin import Langevin
from ase.io import read, write
#from ase.io.lammpsdata import read_lammps_data
import numpy as np
import time
import sys
import os
from ase import Atom, Atoms
from ase.build import bulk
#from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
#from ase.calculators.lammpsrun import LAMMPS
#from ase.calculators.mixing import SumCalculator
from ase.io.jdftx import write_jdftx_IonLattInputs
import glob
#from ase.calculators.mace import MACECalculator
from mace.calculators import MACECalculator
import matplotlib.pyplot as plt

model_path4 = '/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC5_Iter1to12data/MACE_model.model'
model_path2 = '/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC14_JC_3_24JAN24_NVT_NPT_initdataDELTAplusWater_test15conv/2/MACE_model.model'
model_path3 = '/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC14_JC_3_24JAN24_NVT_NPT_initdataDELTAplusWater_test15conv/1/MACE_model.model'
model_path1 = '/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC14_JC_3_24JAN24_NVT_NPT_initdataDELTAplusWater_test15conv/0/MACE_model.model'

#os.system('rm md.xyz')
sysNum = sys.argv[1]
#pattern = 'md*.xyz'
#cat = f'cat {pattern} > md.xyz'
#os.system(cat)
frames = read('md.xyz', ':')

deviation=[]
averages = []
max_deviations = []
candidate_frames = []
candidate_frame_indices = []
currnetPath = []
CandidatePath = []
totalcount = 0
count = 0
for i in range(0, len(frames)):

    if i%1==0:
        print(f'processing frame {i} of {len(frames)} ...')
        frame = frames[i]
        #print(frame)
        MCcalc1 = MACECalculator(model_path=model_path1, device='cuda')
        MCcalc2 = MACECalculator(model_path=model_path2, device='cuda')
        MCcalc3 = MACECalculator(model_path=model_path3, device='cuda')

        # lammps is constant among all 3 models 
        frame.calc=MCcalc1
        f1 = frame.get_forces()
        frame.calc=MCcalc2
        f2 = frame.get_forces()
        frame.calc=MCcalc3
        f3 = frame.get_forces()
        fs = np.stack((f1,f2,f3),axis=0)
        #abrolute
        deviation = np.linalg.norm(np.std(fs, axis=0), axis=-1)
        #real_f = f1
        #deviation = np.linalg.norm(np.sqrt(np.mean(np.square(fs - real_f), axis=0)), axis=-1)
        #magnitude = np.linalg.norm(real_f, axis=-1)
        #deviation = np.linalg.norm(np.std(fs, axis=0), axis=-1)
        #magnitude = np.linalg.norm(np.mean(fs, axis=0), axis=-1)
        #relative = 1
        #deviation /= magnitude + relative
        #print(deviation)
        average_deviation = np.mean(deviation)
        max_deviation = np.max(deviation)
        averages.append(average_deviation)
        max_deviations.append(max_deviation)
        #print(f'Average deviation = {average_deviation}')
        #print(f'Max deviation = {max_deviation}')

        if max_deviation >=0.03 and max_deviation <=0.05:
            #if count > 40: # limit to 40 candidates
            #    break
            count += 1
            #candidate_frames.append(frame)
            candidate_frame_indices.append(i)
            currentPath=os.getcwd()
            #print(f'count is {count}')

#print(f'Candidate count for frame {i} = {count}')
print('All frames processed')
print(f'Total frames in 0.03-0.05 of system {sysNum}= {count}')
print(f'Those frames are {candidate_frame_indices}')
print(f'Average deviations by frame = {averages}')
print(f'Max force deviations by frame (relative) = {max_deviations}')
'''
if count > 40:
    print('Found more than 40 candidates, selecting 40 at random')
    random40frames = np.random.choice(candidate_frame_indices, 40, replace=False)
    print(f'Random 40 frames = {random40frames}')
else:
    random40frames = candidate_frame_indices

count = 0

for i in random40frames:
    frame = frames[i]
    CandidatePath = f'{currentPath}/../../ConfigsForAIMD/sys{sysNum}/{count}'
    print(f'Creating {CandidatePath}'   )
    if not os.path.exists(CandidatePath):
        os.mkdir(CandidatePath)
    else:
        print(f'Error: {CandidatePath} already exists')
    write_jdftx_IonLattInputs(f'{CandidatePath}/md', frame)
    write(f'candidate_{count}.xyz', frame)
    print(f'max deviation for candidate {count} = {max_deviations[i]}')
    count += 1
'''
plt.figure()
plt.hist(max_deviations, bins=100, alpha=0.7, edgecolor='k')
plt.title(f'Max deviations for system {sysNum}')
plt.xlabel('Max deviation')
plt.ylabel('Frequency')
plt.savefig(f'abs_hist_max_deviation_{sysNum}.pdf', format='pdf',bbox_inches='tight')

plt.figure()
plt.scatter(range(0,len(max_deviations)), max_deviations)
plt.title(f'Max deviations for system {sysNum} over time')
plt.xlabel('Frame')
plt.ylabel('Max deviation')
plt.savefig(f'abs_scatter_max_deviation_{sysNum}.pdf', format='pdf',bbox_inches='tight')

'''if os.path.exists('candidates.xyz'):
   os.system('rm candidates.xyz')

os.system('cat candidate_*.xyz > candidates.xyz')'''
