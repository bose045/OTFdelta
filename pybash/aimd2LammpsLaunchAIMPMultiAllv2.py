#!/usr/bin/env python

## 2-2-2023 updated to convert output to both jdftx and outcar for dpmd or snn use

# module load python/3.11 openmpi lammps
# swap for "openmpi-gpu" if you run on a single core or on gpu3001 - like with deepmd 
# module load python/3.11 openmpi-gpu lammps

import numpy as np
import sys
import gzip
import os
import glob

# python /gpfs/u/home/XXXX/XXXXxxxx/scratch-shared/PolyGroup/DeltaLearning/aimd2LammpsLaunchAIMPMultiAll.py sys0_run0001_0000_0000.jdftxout.gz

# if len(sys.argv)<1:
#     print('Usage: aim2....py <jdftx.gz>')
#     exit(1)
# titles = []
# os.chdir(r'/home/kamron/DFT/LQ_lammps/')
pattern = r'*gz'
# inFile = sys.argv[1]

# pattern = r'*jdftxout'
# initDataFile = r'init.data'
# currDataFile = r'current.data'
i=0


atomDict = {'C':1, 'F':2, 'H':3, 'O':4, 'Pt':5, 'S':6}
#atomDict = {'Ag':1, 'C':2, 'F':3, 'H':4, 'O':5, 'Pt':6, 'S':7}
# atomDict = {'Cl':1, 'Na':2}

#works:
# with open(currDataFile,"w") as f:
#     for line in initHeader:
#         f.write(line)
#     f.write("XXXXXXXXXXXX")
#     for line in initFooter:
#         f.write(line)

# initFooter

# TODO add cycle through all folders - systems would all need same # of atom types
# change folder
# print(sorted(glob.iglob(os.path.join(os.getcwd(), pattern))))

# Cycle through cwd for all aimd jdftxout files (delta in this case)
for pathAndFilename in sorted(glob.iglob(os.path.join(os.getcwd(), pattern))):

# if True:
    i+=1
    inFile = os.path.basename(pathAndFilename)
    title, ext = os.path.splitext(inFile)
    print(title)

    # 
    # titles.append(title[:-4])
    # os.chdir(r'/home/kamron/DFT/LQ_lammps/')
    # inFile = 'md.o105016'
    # baseOutFile = 'o105016'
    # inFile = sys.argv[1] #JDFTx format filename
    # baseOutFile = inFile[3:]
    baseOutFile = title
    # outFileOutcar = baseOutFile + '.outcar' # vasp
    outFileJdftx = baseOutFile + '_Delta.jdftxout' # jdftxoutput
    outFileDump = baseOutFile + '_Delta.dump' # lammps dump to visualize forces
    # initDataFile = baseOutFile + '.data' 
    # initDataFile = '2so3+1hso3-cn_h2o_500-out1.data' # set to the family of bonded systems
    try:
        # initDataFile = os.path.basename(glob.glob(r'2so3+1hso3-cn_h2o_500-out1AllValuesR1.data')[0])
        initDataFile = os.path.basename(glob.glob(r'*out1.data')[0])
    except:
        initDataFile = None
    # initDataFile = os.path.basename(glob.glob(r'2so3+1hso3-cn_h2o_500-out1.data')[0])
    
    readHeader = True  # start reading init data header
    readFooter = False
    initHeader = []
    initFooter = []

    # Read in header (atom and bond types) and footer (coeffs, bonds, dihedrals)
    if initDataFile is not None:
        with open(initDataFile,"r") as f:
            # print(1)
            for line in f:
                # print(line)
                if line.find('xhi') > 0:
                    # Done reading header
                    readHeader = False
                if line.startswith('Masses'):
                    # start reading footer
                    readFooter = True
                if readHeader:
                    initHeader.append(line)
                if readFooter:
                    initFooter.append(line)



    # Dict should also match the jdftxout orig file to preserve order???
    # Dictionary for atoms must match init.data generation from LDFG.py config
    # They should be ***alphabetical***
    # and later match the type/potential assignments for lammps file
    # and then also match 
    # TODO we could define this based on lammps data file

    # Units:
    eV = 1./27.2114  # div to go from (Eh) Hartree to eV    27eV = 1eH
    Angstrom = 1/0.5291772  # div to go from Bohr to Ang.  0.5 Ang =1 Bohr
    kcalPermolToeV = 23.06 #div by to go from kcal/mol to eV.  1 eV to 23.06 kcal/mol

    # Read JDFTx input and convert to VASP
    nSteps = 0  # number of processed steps
    nEvery = 10  # select this stride length in frames
    stepActive = False  # Whether to process current data
    latvecActive = False  # Whether reading lattice vectors
    stressActive = False  # Whether reading stress tensor
    atposActive = False  # Whether reading atomic positions
    forcesActive = False  # Whether reading forces
    # headerWrittenoutcar = False
    headerWrittenjdftx = False
    rdfInited = False
    converged = False  # check for convergence before allowing data taken



    def writeLatticeJdftx(R, fp):
        print('R = ', file=fp)
        for i in range(3):
            print('[{:13.4f}{:13.4f}{:13.4f} ]'.format(*tuple(R[i])), file=fp)
                  
    fpoutJdftx = open(outFileJdftx, "w")
    fpoutDump = open(outFileDump, "w")
    fpIn = gzip.open(inFile, 'rt') if (inFile[-3:]==".gz") else open(inFile,'r')
    for iLine, line in enumerate(fpIn):
        # print(line)
        if line.find('total atoms') > 0:
            nAtoms = int(line.split()[4])
        # ElecMinimize: None of the convergence criteria satisfied after 30 iterations.
        # or ElecMinimize: Converged (but not with SCF!)
        if line.startswith('ElecMinimize: Converged'):
            converged = True
        if line.startswith('IonicDynamics: Step:'):
            tokens = line.split()
            iStep = int(tokens[2])  
            if converged:
                stepActive = (iStep % nEvery == 0)# and (not iStep == 0)  # skip first step!
                # print(stepActive)
                converged = False
            PE = float(tokens[4])/eV
            # PE = (float(tokens[4]) - (nAtoms/2)*(E_NaPlus+E_ClMinus))/eV  # how does this compare to the PE in LAMMPS.  I assume that is not adjusted either.  Is this just part of the vasp definition?  number of at pairs/total E ref.
            # XX removed total PE - ref energy for pairs
        # Lattice vectors:
        if latvecActive and iLine<refLine+3:
            iRow = iLine-refLine
            R[iRow] = [ float(tok)/Angstrom for tok in line.split()[1:-1] ]  # convert to Ang from Bohr
            if iRow==2:
                latvecActive = False
        if line.startswith('R ='):
            latvecActive = True
            refLine = iLine+1
            R = np.zeros((3,3))
        # Stress tensor:
        if stressActive and iLine<refLine+3:
            iRow = iLine-refLine
            stress[iRow] = [ float(tok)/(eV/Angstrom**3) for tok in line.split()[1:-1] ]
            if iRow==2:
                stressActive = False
        if stepActive and line.startswith('# Stress tensor in'):
            stressActive = True
            refLine = iLine+1
            stress = np.zeros((3,3))
        # Atomic positions:
        if atposActive and iLine<refLine+nAtoms:
            iRow = iLine-refLine
            tokens = line.split()
            atNames.append(tokens[1])
            atNamesInd.append(atomDict[tokens[1]])
            atpos[iRow] = [ float(tok) for tok in tokens[2:5] ]
            if iRow+1==nAtoms:
                atposActive = False
                if coordsType == "cartesian":
                    atpos *= 1./Angstrom
                else:
                    atpos = np.dot(atpos, R.T) # R in Ang convert to Cartesian (Angstrom)
                atNames = np.array(atNames)
        if stepActive and line.startswith('# Ionic positions in '):
            atposActive = True
            refLine = iLine+1
            atpos = np.zeros((nAtoms,3))  # units are XX
            atNames = []
            atNamesInd = []
            coordsType = line.split()[4]
        # Forces:
        if forcesActive and iLine < refLine + nAtoms:
            iRow = iLine-refLine
            tokens = line.split()
            forces[iRow] = [float(tok) for tok in tokens[2:5]]  
            if iRow+1==nAtoms:
                forcesActive = False
                if coordsType == "Cartesian":
                    forces *= 1./(eV/Angstrom)  # convert to eV/Ang from Hartree/Bohr
                else:
                    forces = np.dot(forces, np.linalg.inv(R)/eV)  
                    # R in Ang. convert to Cartesian (eV/Angstrom).  need convert from eH to eV
        if stepActive and line.startswith('# Forces in '):
            forcesActive = True
            refLine = iLine+1
            forces = np.zeros((nAtoms,3))
            coordsType = line.split()[3]

        # Below marks when we complete a section of data and are ready to output data to file and run lammps
        if stepActive and line.startswith("# Energy components:"):
            # Write Lammps data file here (for each time step) with positions 
            # Save sample points to out file
            # First check that the structure is orthorhombic XX

            activeName = baseOutFile + '_' + str(nSteps)
            activeNameFile = activeName + r'.data'
            with open(activeNameFile,"w") as f:
                if initDataFile is not None:
                    for line in initHeader:
                        f.write(line)
                else:
                    f.write("ITEM: TIMESTEP\n")
                    f.write("  %s atoms\n"% (str(nAtoms)))
                    f.write("  6 atom types\n")
                        
                f.write("0 %s xlo xhi\n"% (str(R[0,0])))
                f.write("0 %s ylo yhi\n"% (str(R[1,1])))
                f.write("0 %s zlo zhi\n"% (str(R[2,2])))
                print(f'{str(R[0,1])} {str(R[0,2])} {str(R[1,2])} xy xz yz', file=f)
                # add later tilts from lammps triclinic a = (xhi-xlo,0,0); b = (xy,yhi-ylo,0); c = (xz,yz,zhi-zlo).
                f.write("\n")
                f.write("Masses\n\n")
                f.write("1 12.01\n")
                f.write("2 19.0\n")
                f.write("3 1.01\n")
                f.write("4 16.0\n")
                f.write("5 195.1\n")
                f.write("6 32.06\n")
                f.write("\n")
                f.write("Atoms\n")
                f.write("\n")
                for i in range(nAtoms):
                    f.write("%s %s %s %s %s %s %s\n"% (str(i+1),
                                                      str(1),
                                                      str(atNamesInd[i]),
                                                      str(0),
                                                      str(atpos[i][0]),
                                                      str(atpos[i][1]),
                                                      str(atpos[i][2])))  # index,molec #, type, 0(charge), x, y, z
                f.write("\n")
                
                if initDataFile:
                    for line in initFooter:
                        f.write(line)
            print(activeNameFile)
            print(activeName)
