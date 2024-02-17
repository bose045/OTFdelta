#!/bin/bash/
cd initSysAIMD
for file in init*.jdftxout; do python ../pybash/jmd2allpos.py -f $file; done
