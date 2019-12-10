#!/bin/bash

#$ -pe mpi-24 48             # Specify parallel environment and legal core size
#$ -q *@@schneider_d12chas   # Specify queue
#$ -N dyneb                  # Specify job name

module load vasp/5.4.1

# You will need to update these
export PYTHONPATH=/afs/crc.nd.edu/user/j/jcrum/.local/lib/python3.7/site-packages/:$PYTHONPATH
export PATH=/afs/crc.nd.edu/user/j/jcrum/.local/lib/python3.7/site-packages/ase/tools:$PATH
export ASE_VASP_COMMAND="mpirun vasp_neb"

source ~/.bashrc

echo "Job Started at:"
date

python run_sella.py

echo "Job Ended at:"
date
