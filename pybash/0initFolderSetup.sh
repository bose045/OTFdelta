#!/bin/bash
for i in {0..8};do
    mkdir -p deltaProcess/sys$i
    mkdir -p NNmd/sys$i
    mkdir -p AIMD/sys$i
    mkdir -p ConfigsForAIMD/sys$i
done
mkdir -p maceTrainPotential/{seed0,seed1,seed2}
#mkdir DpmdTrainPotential/train/data
