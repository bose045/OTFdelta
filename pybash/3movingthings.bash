#!/bin/bash
mkdir train
mv ./*Delta.jdftxout ./train
mkdir nondelta
find . -maxdepth 1 -type f -regex '.*\.jdftxout' ! -regex '.*_Delta\.jdftxout' -exec mv {} ./nondelta \;
mkdir gzip
mv ./*gz ./gzip
mkdir vasp
mv ./*vasp ./vasp
mkdir lammpsdata
mv ./*dump ./lammpsdata
mv ./*data ./lammpsdata 
