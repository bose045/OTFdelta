#!/bin/bash

cd ./deltaProcess
# Loop from 0 to 7
for i in {0..7}; do
    cd sys$i
    mv ./*Delta.jdftxout ../../DpmdTrainPotential/train
    cd ..
done

# Handle the case for i = 8
cd sys8
mv ./*jdftxout ../../DpmdTrainPotential/train
cd ..



#mkdir train
#mv ./*Delta.jdftxout ./DpmdTrainPotential/train
#cp ../groundzero/water/*jdftxout ./DpmdTrainPotential/train/
#mkdir nondelta
#find . -maxdepth 1 -type f -regex '.*\.jdftxout' ! -regex '.*_Delta\.jdftxout' -exec mv {} ./nondelta \;
#mkdir gzip
#mv ./*gz ./gzip
#mkdir vasp
#mv ./*vasp ./vasp
#mkdir lammpsdata
#mv ./*dump ./lammpsdata
mv ./*data ./lammpsdata 
