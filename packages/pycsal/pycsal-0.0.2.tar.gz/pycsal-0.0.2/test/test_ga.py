import unittest
import sys
from ase import Atoms, Atom
from ase.data import atomic_numbers
from ase.ga.data import PrepareDB, DataConnection
from ase.io import read
from ase.calculators.emt import EMT
from ase.optimize import FIRE,BFGS
from ase.constraints import ExpCellFilter
import os
from ase.calculators.singlepoint import SinglePointCalculator
from ase.ga import set_raw_score, get_raw_score

class TestGA(unittest.TestCase):
    def test_ga_create_database(self):
        ###parameters
        ele = ['Mg', 'Sn']
        Natom = [4, 1] 
        syss = read('out0.xyz', index=":", format = 'extxyz')   
        database='gadb.db'
        relaxed=False    
        #####
        if os.path.exists(database):
            os.system('rm ' + database)
        blocks = []
        Z = []

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
        print(syss[0])

    def test_relax(self):
        def finalize(atoms, calculator, energy=None, forces=None, stress=None):
            # Finalizes the atoms by attaching a SinglePointCalculator
            # and setting the raw score as the negative of the total energy
            #print('call finalize ', atoms,flush=True)
            atoms.wrap()
            calc = SinglePointCalculator(atoms, energy=energy, forces=forces,
                                        stress=stress)
            #print('call SinglePointCalculator ', atoms,flush=True)
            atoms.calc = calc## use calulator to calcualte the final sing-point energy
            try:
                raw_score = -atoms.get_potential_energy() #
            except:
                raw_score = -1e9
            set_raw_score(atoms, raw_score)
            #print('finalize ', atoms, raw_score,flush=True)
        ###input
        step = 0
        restart = False
        calculator = EMT()
        fitter = calculator
        cellbounds = None
        lat = [3, 3, 3, 90, 90, 90]
        ####
        atoms = Atoms( [Atom('Ag', [0, 0, 0]), Atom('Ag', [0, 0, 1.0])] , cell = lat, pbc=True  )
        print('step restart', step, restart, flush=True)
        if step == 0 or restart == True:
            atoms.calc = calculator
        else:
            atoms.calc = fitter
        if restart == False:
            converged = False
            niter = 0
            print('relax ', atoms, atoms.get_potential_energy(), flush=True)
            while not converged and niter < 10:
                if cellbounds is not None:
                    cell = atoms.get_cell()
                    if not cellbounds.is_within_bounds(cell):
                        niggli_reduce(atoms)
                    cell = atoms.get_cell()
                    if not cellbounds.is_within_bounds(cell):
                        # Niggli reduction did not bring the unit cell
                        # within the specified bounds; this candidate should
                        # be discarded so we set an absurdly high energy
                        print('discard within bounds', atoms.cell.cellpar())
                        finalize(atoms, calculator, 1e9)
                        
                        return 1e9
                print('niter', niter)
                ecf = ExpCellFilter(atoms)
                #print('BFGS')
                dyn = BFGS(ecf, logfile='opt.log', trajectory=None)
                atoms.set_pbc([True, True, True])
                #print('dyn.run pbc', atoms.get_pbc(), atoms.cell.cellpar(), flush=True)
                #try:
                dyn.run(fmax=1e-1, steps=10) #1e-2 -> 1e-1
                converged = dyn.converged()
                #except:
                #    print('exit from dyn.run', atoms)
                #    break
                niter += 1
            dyn = BFGS(atoms, logfile='opt.log', trajectory=None)
            dyn.run(fmax=1e-3, steps=200)
            dyn = FIRE(atoms, logfile='opt.log', trajectory=None)
            dyn.run(fmax=1e-3, steps=200)

        atoms.calc = calculator
        ##remove WAVECAR for different structures to avoid error
        if os.path.exists('WAVECAR'):
            os.system('rm WAVECAR')

        e = atoms.get_potential_energy()
        #except:
        #    return 1e7
        print('energy-system:', e, atoms, flush=True)
        f = atoms.get_forces()
        s = atoms.get_stress()
        #print('after relax: ', e)
        finalize(atoms, calculator, energy=e, forces=f, stress=s)
        return e

if __name__ == '__main__':
    unittest.main()