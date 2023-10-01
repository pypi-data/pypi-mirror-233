from ase import Atoms
from ase.data import atomic_numbers
from ase.ga.utilities import closest_distances_generator, CellBounds
#from ase.ga.startgenerator import StartGenerator
from ase.ga.data import PrepareDB, DataConnection

from pycsal.gen_stru import gen_V, gen_ase
from ase.calculators.lammpslib import LAMMPSlib
import os
from ase.io.vasp import read_vasp, write_vasp
import numpy as np

from ase.build import niggli_reduce
from ase.calculators.singlepoint import SinglePointCalculator
from ase.optimize import FIRE,BFGS,BFGSLineSearch, GPMin
from ase.constraints import ExpCellFilter
from ase.ga import set_raw_score, get_raw_score

try:
    from asap3 import EMT
except ImportError:
    from ase.calculators.emt import EMT

from ase.io import write, extxyz
from ase.ga.population import Population
from ase.ga.ofp_comparator import OFPComparator
from ase.ga.offspring_creator import OperationSelector
from ase.ga.standardmutations import StrainMutation
from ase.ga.soft_mutation import SoftMutation
from ase.ga.cutandsplicepairing import CutAndSplicePairing
Nstep = 5
ele = ['Mg', 'Sn']
Natom = [4, 1]
database = 'gadb.db'
rcut = 0.5
population_size = 20
cmds = ["pair_style meam",
        "pair_coeff * * library.meam Mg Sn  MgSn.meam Mg Sn"]
lammps = LAMMPSlib(lmpcmds=cmds, logfile='test.log', keep_alive = True )
calculator = lammps  ## target potential, MEAM/DFT
fitter = lammps

class TestGA(unittest.TestCase):

    def ga_create_database(ele, Natom, syss, database='gadb.db', relaxed=False):
        blocks = []
        Z = []
        #stoichiometry = []
        for i in range(len(ele)):
            blocks = blocks + [ele[i]] * Natom[i]
            #Z.append(atomic_numbers[ele[i]])
        for i in range(len(blocks)):
            Z.append(atomic_numbers[blocks[i]])
        # Create the database
        da = PrepareDB(db_file_name=database, stoichiometry= Z)
        for sys in syss:
            if relaxed == False:
                da.add_unrelaxed_candidate(sys)
            elif relaxed == True:
                da.add_relaxed_candidate(sys)            
    

#    def test_GA_run():
#        ga_opt(Nstep, ele, Natom, calculator, fitter, cellbounds=None, database=database, population_size = population_size, out=None, rcut=rcut )

#    def test_upper(self):
#        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()