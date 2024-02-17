#!/bin/bash
#SBATCH -N 1 -n 1 -t 1 --gres=gpu:1 -o md.o%j

touch allMDjobsDone
