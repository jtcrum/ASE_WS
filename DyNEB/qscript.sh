#!/bin/bash

#$ -pe mpi-48 96             # Specify parallel environment and legal core size
#$ -q *@@schneider_d24cepyc  # Specify queue
#$ -N dyneb                  # Specify job name

module load vasp/5.4.1

# Update the directories to your directories
export PYTHONPATH=/afs/crc.nd.edu/user/j/jcrum/.local/lib/python3.7/site-packages/:$PYTHONPATH
export PATH=/afs/crc.nd.edu/user/j/jcrum/.local/lib/python3.7/site-packages/ase/tools:$PATH
export ASE_VASP_COMMAND="mpirun vasp_neb"

source ~/.bashrc

echo "Job Started at:"
date

python run_dyNEB_vasp.py

echo "Job Ended at:"
date
