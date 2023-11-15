#!/bin/bash
# multiLDFG.sh

for f in *.vasp; do

    python /global/homes/k/kamron/LammpsDataFileGeneratorKF/LDFG.py $f
    
done