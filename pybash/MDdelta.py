from ase import units
from ase.md.langevin import Langevin
from ase.io import read, write
from ase.io.lammpsdata import read_lammps_data
import numpy as np
import time
import sys
import os
from ase import Atom, Atoms
from ase.build import bulk
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
#from ase.md.nptberendsen import  NPTBerendsen
from ase.md.npt import NPT
from ase.calculators.lammpsrun import LAMMPS
# from deepmd.calculator import DP
from ase.calculators.mixing import SumCalculator


from mace.calculators import MACECalculator

#model_path='/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC13_OTF1_iter1to12DeltaSys1_2_3onlyBonds/MACE_model.model'
#model_path='/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC14_JC_3_24JAN24_NVT_NPT_initdataDELTAplusWater_test15conv/0/MACE_model.model'
model_path='/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/maceOTFdelta/Autolearn/latestModel/seed0/MACE_model.model'
MCcalc = MACECalculator(model_paths=model_path, device='cuda')

datain = sys.argv[1]
sysNum = sys.argv[2]
runIter = sys.argv[3]

# attempt 100 seeded runs
for i in range(100):

        keepRunning = False  # remains false if no sim failure in Fmax occurs

        ats = read_lammps_data(datain)
        # [1:12,2:19,3:1,4:16,5:195,6:32]
        print(ats.get_chemical_symbols())

        files = [datain+'START',datain+'END']

        os.system(f'rm md_{runIter}_{sysNum}.xyz')

        lammps = LAMMPS(files=files)

        lammps.parameters['units']='metal'
        lammps.parameters['atom_style']='full'
        lammps.parameters['bond_style']='harmonic'
        # delta:
        ats.calc = SumCalculator([MCcalc,lammps])

        # Set the momenta corresponding to cooler value
        MaxwellBoltzmannDistribution(ats, temperature_K=300)

        dt = 0.1 # fs
        dyn = Langevin(ats, dt*units.fs, temperature_K=300, friction=0.001/units.fs) # was 5e-3
        #dyn = NPTBerendsen(atoms, timestep=dt * units.fs, temperature_K=300,taut=100 * units.fs, pressure_au=1.01325 * units.bar,taup=1000 * units.fs, compressibility_au=4.57e-5 / units.bar)
        #sigma = 1.0
        #ttime = 20.0
        #pfactor = 2e6
        #dyn = NPT(ats,dt*units.fs,temperature_K=300,externalstress=sigma*units.bar, ttime=ttime*units.fs,pfactor=pfactor*units.GPa*(units.fs**2))
        
        def write_frame():
                # dyn.atoms.write('md.xyz', append=True)
                dyn.atoms.write(f'md_{runIter}_{sysNum}.xyz', append=True)
        # dyn.attach(write_frame, interval=2)
        # dyn.run(5000)
        intervalfs=50 # interval in fs to save
        dyn.attach(write_frame, interval=int(intervalfs/dt))

        fsToRun = 50000
        fsPerCycle = 5
        for runs in range(int(fsToRun/fsPerCycle)):
                dyn.run(int(fsPerCycle/dt)) # was 10e3 fs was 50k
                atForces = ats.get_forces()
                # check forces
                # if forces too high break
                # print(np.mean(atForces, axis=1))
                forcesMag = np.linalg.norm(atForces,axis=1)
                forcesMagMax = np.max(forcesMag)
                print('forcesMagMax ', forcesMagMax)
                print('fs ', (runs+1)*fsPerCycle)
                if forcesMagMax > 1000: 
                        keepRunning = True  # allow another attempt to be made
                        break

        # ramains false unless failed forceMag too high
        if not keepRunning:
                break


print("MD finished!")


# atdone = read('md.xyz', '0')
# atdone.set_chemical_symbols('Pt'*36+'S'*2+'O'*31+'C'*6+'F'*14+'H'*48)
# atdone.write('md2.xyz','')


# from mace.calculators import MACECalculator

# calculator = MACECalculator(model_path='/global/homes/k/kamron/Scratch/AIMDtoNN/Poly/PolyMC2wHighP/MACE_model.model', device='cuda')
# init_conf = read('/global/homes/k/kamron/Scratch/NNmd/Poly/MC3polyPtWater/500deg300rot.xyz', '0')
# # init_conf = read('BOTNet-datasets/dataset_3BPA/test_300K.xyz', '0')
# init_conf.set_calculator(calculator)

# dyn = Langevin(init_conf, 0.5*units.fs, temperature_K=310, friction=5e-3)
# def write_frame():
#         dyn.atoms.write('md.xyz', append=True)
# dyn.attach(write_frame, interval=20)
# dyn.run(2e3)
# print("MD finished!")
