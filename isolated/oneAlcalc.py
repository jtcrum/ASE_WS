from ase import Atoms, Atom
from vasp import Vasp
from vasp.vasprc import VASPRC
import numpy as np
from ase.io import write
import matplotlib.pyplot as plt
from ase.io import read
import os
from ase.io import read
from ase.constraints import FixAtoms
from ase.io.vasp import write_vasp
import math
import shutil
from ase.build import molecule

VASPRC['queue.pe'] = 'mpi-48'
VASPRC['queue.nprocs'] = 48
VASPRC['queue.q'] =  '*@@schneider_d24cepyc'

lattice=read('./CONTCAR')

total_Oxygen = np.arange(1,73);
Aluminium = [0]
total_Silicon = np.arange(73,108)
Hydrogen = [108]

lattice=read('./CONTCAR')

First_Oxygens = [46, 51, 84, 97]



Energy=[]
Position=[]
cwd = os.getcwd()
for l in range(4):

    #move to the directory of each structure
    path='D-'+ str(First_Oxygens[l])
    a=read(cwd+'/'+path+'/POSCAR')
    a=Atoms(a)
    calc = Vasp(cwd+'/'+path+'/CALC1',
        encut = 400,
        sigma = 0.1,
        ediffg = -.05,
        ediff = 1e-6,
        ismear = 0,
        nsw = 500,
        ncore=6,
        ibrion = 2,
        lwave = False,
        lcharg = False,
        lreal = 'A',
        atoms=a)

    Energy.append(a.get_potential_energy())
    Position.append(str(First_Oxygens[l]))


if None in Energy:
    calc.abort()

print(r'| Position ($\AA$)| Energy (eV)|')
for P, e in zip(Position, Energy):
    print('| {0} | {1} |'.format(P, e))

for e in Energy:
    print('{}'.format(e))
