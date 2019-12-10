import os
from ase.calculators.vasp.vasp2 import Vasp2 as vasp_calculator
from ase.io import read

from sella import Sella

atoms = read('path to transitions state CONTCAR')

calc = vasp_calculator(
       istart = 1,
       prec = 'Accurate',
       encut = 400,
       xc = 'PBE',
       lcharg = False,
       directory = 'path to sell run folder')

atoms.set_calculator(calc)

dyn = Sella(atoms,
            trajectory ='test_vasp2.traj')

dyn.run(1e-3, 1000)
