#!/bin/bash
for i in {0..8};do
    mkdir -p deltaProcess/sys$i
    mkdir -p NNmd/sys$i
    mkdir -p ConfigsForAIMD/sys$i
done
mkdir -p AIMD
mkdir -p DpmdTrainPotential/{train,seed0,seed1,seed2,seed3}
mkdir DpmdTrainPotential/train/data
