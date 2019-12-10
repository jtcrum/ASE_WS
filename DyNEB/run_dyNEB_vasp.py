import os
from ase.neb import NEB
from ase.io import read, write
from ase.calculators.vasp.vasp2 import Vasp2 as vasp_calculator
from ase.optimize import BFGS
import numpy as np
from ase import Atoms, atom
import glob

# Number of NEB interior images
nimages = 4
images = []



r = read('path to reactants OUTCAR')
p = read('path to products OUTCAR')


# Read in the endstates and prepare the band.
# The endstates traj  files should contain energy and forces
# Instead of .traj files e.g. OUTCAR can be read
images = [r]
for i in range(nimages):
    images.append(r.copy())
images.append(p.copy())

# Define the calculator
def calculator(imgdir):
    return vasp_calculator(
           istart=1,
           encut=400,
           xc='PBE',
           ediff = 1e-4,
           lvhar=False,
           lcharg=False,
           lasph=False,
           lreal = 'A',
           directory=imgdir)


# Initialize the NEB class with the dynamic keyword
#neb = NEB(images, dynamic_relaxation=True, scale_fmax=1.)

# Interpolate the interiorimages
#neb.interpolate('idpp',mic=True)

# Give each image its respective directory and assign a calculator
home = os.getcwd()
for i in range(nimages+2):
    imgdir = '%02d' % i
    if imgdir not in os.listdir(home):
        os.mkdir(imgdir)
    write(imgdir+'/POSCAR', images[i])
    if i not in [0, nimages+1]:
        images[i].set_calculator(calculator(imgdir))

# Run without climbing
#opt = BFGS(neb, trajectory='neb_noclimb.traj', logfile='neb_noclimb.log')
#opt.run(fmax=0.05)
#write('Final_NEB_non_climbed.traj', images)

# Run with climbing and tighter convergence
neb = NEB(images, dynamic_relaxation=True, scale_fmax=2.,
          fmax=0.03, climb=True)

opt = BFGS(neb, trajectory='neb_climb.traj', logfile='neb_climb.log')
opt.run(fmax=0.03)
write('Final_NEB_climbed.traj', images)
