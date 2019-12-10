# -*- coding: utf-8 -*-

from ase.io import read
from ase import Atoms, Atom
from ase.constraints import FixAtoms
from ase.io.vasp import write_vasp
import math
import os.path
import numpy as np
import os
import shutil
from ase.build import molecule
from ase.visualize import view

##############################################################################

lattice=read('./CONTCAR')
atoms = Atoms(lattice)

total_Oxygen = [atom.index for atom in atoms if atom.symbol=='O']
Aluminium = [atom.index for atom in atoms if atom.symbol=='Al']
total_Silicon = [atom.index for atom in atoms if atom.symbol=='Si']
Carbon = [len(atoms)]
Hydrogen = [len(atoms)+1, len(atoms)+2, len(atoms)+3]

Oxygens = []
for j in Aluminium:
    tmp = []
    for k in total_Oxygen:
        distance = lattice.get_distance(j,k,mic=True)
        if distance < 2.0:
            tmp.append(k)
            if len(tmp) == 4:
                Oxygens.append(tmp)
                tmp = []
Oxygens = np.array(Oxygens) #convert array to numpy style
print ('First_Oxygens = ' + str(Oxygens[0]))
First_Oxygens = Oxygens[0]

Silicons = []
for l in Oxygens[0]:
    tmp = []
    for m in total_Silicon:
        distance = lattice.get_distance(l,m,mic=True)
        if distance < 2.0:
            Silicons.append(m)
Silicons = np.array(Silicons) #convert array to numpy style
print ('First_Silicons = ' + str(Silicons))
First_Silicons = Silicons

#Create Directories for all Possible Oxygen-Hydrogen Locations

adsorbate = molecule('C')
adsorbate.translate([0, 0, 0])
H_lattice = lattice + adsorbate

cwd = os.getcwd()

for l in range(4):
    H_lattice = lattice + adsorbate
    center = H_lattice.get_center_of_mass()
    positions = atoms.get_positions()
    diff = center - positions[Aluminium]
    p1 = H_lattice.get_positions()
    H_lattice.translate(diff)
    H_lattice.wrap()
    H_lattice.set_distance(First_Oxygens[l], Carbon[0], 1.5, fix=0)
    H_lattice.set_angle([Aluminium[0], First_Oxygens[l], Carbon[0]], np.pi/1.643, mask=None)
    H_lattice.set_angle([First_Silicons[l], First_Oxygens[l], Carbon[0]], np.pi/1.643, mask=None)
    H_lattice.set_dihedral([Aluminium[0], First_Oxygens[l], First_Silicons[l], Carbon[0]], np.pi, mask=None)
    H_lattice.translate(-1*diff)
    H_lattice.wrap()
    p2 = H_lattice.get_positions()
    diff2 = p2[Carbon]-p1[Carbon]
    adsorbate2 = molecule('CH3')
    adsorbate2.translate([0,0,0])
    adsorbate2.translate(diff2)
    H_lattice = lattice + adsorbate2
    
    # makes directory of each First_Oxygen-Second_Oxygen case with terminal hydrogen
    if not os.path.exists(cwd + '/D-' + str(First_Oxygens[l])):
        os.mkdir(cwd + '/D-' + str(First_Oxygens[l]))

    # move to made directory from working directory of this script
    os.chdir(cwd + '/D-' + str(First_Oxygens[l]))

    #write POSCAR format of hydrogen terminated and Al-substituted zeolite framework
    #copy INCAR, POTCAR, KPOINTS and c-shell script to each directory of Si(T-site)-Oxygen case
    write_vasp('POSCAR'.format(First_Oxygens[l]), H_lattice, label = '', direct=True, sort=True, symbol_count=None, long_format=True, vasp5=False)

    # move back to the working directory of this script
    os.chdir(cwd)
