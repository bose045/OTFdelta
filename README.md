# OTFdelta

## Environment setup:


    deepmd kit and deepmd lammps
    conda create -n deepmd deepmd-kit=*=*cpu libdeepmd=*=*cpu lammps -c https://conda.deepmodeling.com -c defaults


    for converting into deepmd from jdftx output:
    git clone https://github.com/KamronF9/dpdatajdftx
    python -m pip install -e .

    sudo apt-get install libgsl-dev
    sudo apt-get install libfftw3-dev libfftw3-doc
    sudo apt-get install libblas-dev liblapack-dev
    git clone https://github.com/shankar1729/jdftx.git jdftx-git
    [in build dir]cmake ../jdftx-git/jdftx
    make
    export PATH="/home/kamron/DFT/jdftx/build:/home/kamron/DFT/jdftx/jdftx-git/jdftx/scripts:$PATH"

    conda install -c conda-forge octave (for jdftx createxsf)

## Folder structure setup

- Autolearn (start here and run AutoLearnAll.py)
    - DpmdTrainPotential (training data keeps growing and stores latest NNP)
        - train (put initial user AIMD data here as .jdftxout files)

    - 0000
        <!-- - AIMD (user made) initial dataset
            - sys1-4... (each system considered) -->
        - Train
        - NNmd
            - sys1-4... (each system considered)
    - 0001
        - AIMD (new chosen snapshots from 0000-NNmd)
        - Train
        - NNmd

### Files to use across runs
    input.json  
    inputNewRuns.json  
    lammpsNNmd.in  
    md.in  
    singles.job  
    train.job  
    trainNewRuns.job