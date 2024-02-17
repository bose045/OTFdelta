#!/bin/bash

export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1280

for dir in */; do
    cd $dir
    seedNum=$(echo "$dir" | sed 's/\///g')  # remove the / from the folder name
    sbatch ../train.job ${seedNum}
    cd ..
done