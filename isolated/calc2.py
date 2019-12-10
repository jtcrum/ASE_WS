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
VASPRC['queue.q'] =  'hpc'


First_Oxygens = [46,51,84,97]


Energy=[]
Position=[]
cwd = os.getcwd()
for l in range(4):

    #move to the directory of each structure
    path='D-'+ str(First_Oxygens[l])
    calc = Vasp(cwd+'/'+path+'/CALC1')
    atoms = calc.get_atoms()
    calc = Vasp(cwd+'/'+path+'/CALC2')
    '''
                encut = 400,
                sigma = 0.01,
                ediffg = -.01,
                ediff = 1e-6,
                ismear = 0,
                nsw = 500,
                ncore =6,
                ibrion = 1,
                lwave = False,
                lcharg = False,
                lreal = 'A',
                atoms = atoms)
    '''
    steps = calc.get_number_of_ionic_steps()
    if steps >= 500:
        os.system('mv '+path+'/CALC2/CONTCAR '+path+'/CALC2/POSCAR')
        os.system('rm -r '+path+'/CALC2/OUTCAR')
        calc.calculate()
    Energy.append(calc.get_potential_energy())
    Position.append(str(First_Oxygens[l]))

Energy = np.array(Energy)
#Energy -= min(Energy)
if None in Energy:
    calc.abort()

print(r'| Position ($\AA$)| Energy (eV)|')
for P, e in zip(Position, Energy):
    print('| {0} | {1} |'.format(P, e))

for e in Energy:
    print('{}'.format(e))
