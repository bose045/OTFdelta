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

# model_path='/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC5_Iter1to12data/MACE_model.model'
# model_path='MACE_modelPolyMC2wHighPFull.model'
# model_path='/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC8_OTF1_iter1to12DeltaSys1and2/MACE_model40epSys1and2.model'
# model_path='/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC9_OTF1_iter1to12DeltaSys1and2noLJ/MACE_model.model'
model_path='/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC13_OTF1_iter1to12DeltaSys1_2_3onlyBonds/MACE_model.model'
# MCcalc = MACECalculator(model_path='MACE_modelSB001.model', device='cuda')
# MCcalc = MACECalculator(model_path='/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/AIMDtoNN/PolyMC8_OTF1_iter1to12DeltaSys1and2/MACE_model.model', device='cuda')
MCcalc = MACECalculator(model_path=model_path, device='cuda')

# init_conf = read('/global/homes/k/kamron/Scratch/NNmd/Poly/MC3polyPtWater/500deg300rot.xyz', '0')
# # init_conf = read('BOTNet-datasets/dataset_3BPA/test_300K.xyz', '0')
# init_conf.set_calculator(calculator)





# dpcalc=DP(model="round13R9_47k.pb",type_dict={'C':1,'F':2,'H':3,'O':4,'Pt':5,'S':6})
# dpcalc=DP(model="round11extraHr3_8k.pb")

# sys.exit(1)

# export ASE_LAMMPSRUN_COMMAND=/global/u2/k/kamron/.conda/envs/deepmd3/bin/lmp
# meh export ASE_LAMMPSRUN_COMMAND=/home/fazelk/.conda-envs/deepmd/bin/lmp
# export ASE_LAMMPSRUN_COMMAND=/gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/npl_miniconda/envs/deepmd/bin/lmp

# datain='pt+hso3+h2o-frz_8x8_1ML_longHack6wWater.data' # initial run
#datain='md.data' # continuation run files generated from MDdeltaCont.py

datain = sys.argv[1]
sysNum = sys.argv[2]
runIter = sys.argv[3]
# datain='init.data'
# datain='pt+hso3+h2o-frz_8x8_1ML_longHack5.data'
# datain='pt+2so3-cn-frz_vac_500_0deg-out1_4x4.data'
# datain = 'pt+2so3-cn-frz_vac_500_0deg-out1noHObond.data'
# datain = '2so3+1hso3-cn_h2o_500-out1.data'
# datain = '2so3+1hso3_vac_500-out1.data'
# ats = read_lammps_data('pt+2so3-cn-frz_vac_500_0deg-out1NoBOND.data',Z_of_type={'1':'12','2':'19','3':'1','4':'16','5':'195','6':'32'})
# ats = read_lammps_data('pt+2so3-cn-frz_vac_500_0deg-out1NoBOND.data',sort_by_id=False,Z_of_type={1:12,2:19,3:1,4:16,5:195,6:32})
# ats = read_lammps_data('pt+2so3-cn-frz_vac_500_0deg-out1NoBOND.data',Z_of_type={5:195,6:32,4:16,1:12,2:19,3:1})
# ats = read_lammps_data('pt+2so3-cn-frz_vac_500_0deg-out1NoBOND.data',Z_of_type=dict([(1,12),(2,19),(3,1),(4,16),(5,195),(6,32)]))
# ats = read_lammps_data(datain)



# attempt 100 seeded runs
for i in range(2):

        keepRunning = False  # remains false if no sim failure in Fmax occurs

        ats = read_lammps_data(datain)
        # ats = read_lammps_data('pt+2so3-cn-frz_vac_500_0deg-out1NoBOND.data',Z_of_type=dict([(0,12),(1,19),(2,1),(3,16),(4,195),(5,32)]))
        # ats = read_lammps_data('pt+2so3-cn-frz_vac_500_0deg-out1NoBOND.data',Z_of_type=dict([(5,195),(6,32),(4,16),(1,12),(2,19),(3,1)]))
        # print(ats.get_chemical_symbols())
        # ats.set_chemical_symbols('5'*36+'6'*2+'4'*31+'2'*6+'3'*14+'1'*48)
        # ats.set_chemical_symbols('Pt'*36+'S'*2+'O'*31+'C'*6+'F'*14+'H'*48)
        # ats.set_chemical_symbols('Pt'*36+'S'*2+'O'*31+'C'*6+'F'*14+'H'*48)
        # ats.set_chemical_symbols('S'*3+'O'*37+'C'*9+'F'*21+'H'*53)
        # ats.set_chemical_symbols('S'*3+'O'*37+'C'*9+'F'*21+'H'*53)
        # print(ats)
        # [1:12,2:19,3:1,4:16,5:195,6:32]
        print(ats.get_chemical_symbols())
        # atoms.arrays["bonds"]

        # sys.exit(1)

        # bond_style harmonic
        # angle_style harmonic
        # dihedral_style harmonic


        # read_data               ${struc}
        # pair_style lj/cut 5.0
        # include                 VDW_LAMMPS_MD

        # pair_modify tail yes
        # special_bonds	lj/coul 0 0 1.0

        # parameters = {'units': 'metal'}

        # lammps_parameters = {
        #         'units': 'metal',
        #         'atom_style': 'full',
        #         'bond_style': 'harmonic',
        #         'angle_style': 'harmonic',
        #         'dihedral_style': 'harmonic',
        #         'pair_style': 'lj/cut 5.0', 
        #         'include': 'VDW_LAMMPS_MD',
        #         'pair_modify': 'tail yes',
        #         'special_bonds': 'lj/coul 0 0 1',
        #         # 'neigh_modify': 'exclude type 4 5',       
        #         # 'read_data': '2so3+1hso3-cn_h2o_500-out1.data',
        #         # 'read_data': datain,
        #         # 'include': datain,
        #         }

        # parameters = {'pair_style': 'eam/alloy',
        #             'pair_coeff': ['* * NiAlH_jea.eam.alloy H Ni']}

        files = [datain+'START',datain+'END']

        # C = bulk('C', cubic=True)
        # H = Atom('H', position=Ni.cell.diagonal()/2)
        # NiH = Ni + H
        # ase_parameters = {
        #         'tmp_dir': '/home/fazelk/PolyNew/MC4polyPtWaterDelta/temp/',
        #         'keep_tmp_files': 'True',
        #         'verbose': 'True',
        # }



        os.system(f'rm md_{runIter}_{sysNum}.xyz')

        # lammps = LAMMPS(parameters=parameters, files=files)
        # lammps = LAMMPS(files=files,tmp_dir='temp')
        lammps = LAMMPS(files=files)
        # lammps = LAMMPS()

        lammps.parameters['units']='metal'
        lammps.parameters['atom_style']='full'
        lammps.parameters['bond_style']='harmonic'
        # lammps.parameters['angle_style']='harmonic'
        # lammps.parameters['dihedral_style']='harmonic'
        # removed pair styles

        # lammps.parameters['pair_style']='lj/cut 5.0'
        # lammps.parameters['pair_style']='lj/cut/coul/cut 5.0'
        # lammps.parameters['tmp_dir']='temp'

        # lammps=LAMMPS
        # ase_parameters=ase_parameters
        # lammps.set('units': 'metal')
        # single potential pick one:
        # ats.calc=MCcalc
        # ats.calc=dpcalc
        # ats.calc = lammps

        # delta:
        ats.calc = SumCalculator([MCcalc,lammps])
        # print("Energy ", NiH.get_potential_energy())
        # print("Energy ", ats.get_potential_energy())
        # dyn = Langevin(ats, 0.1*units.fs, temperature_K=310, friction=0.01/units.fs) # was 5e-3

        # Set the momenta corresponding to cooler value
        MaxwellBoltzmannDistribution(ats, temperature_K=150)

        dt = 0.1 # fs
        #dyn = Langevin(ats, dt*units.fs, temperature_K=300, friction=0.001/units.fs) # was 5e-3
        #dyn = NPTBerendsen(atoms, timestep=dt * units.fs, temperature_K=300,taut=100 * units.fs, pressure_au=1.01325 * units.bar,taup=1000 * units.fs, compressibility_au=4.57e-5 / units.bar)
        sigma = 1.0
        ttime = 20.0
        pfactor = 2e6
        dyn = NPT(ats,dt*units.fs,temperature_K=300,externalstress=sigma*units.bar, ttime=ttime*units.fs,pfactor=pfactor*units.GPa*(units.fs**2))
        
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
