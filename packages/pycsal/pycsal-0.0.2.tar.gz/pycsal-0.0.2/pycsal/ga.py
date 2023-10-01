from ase import Atoms
from ase.data import atomic_numbers
from ase.ga.utilities import closest_distances_generator, CellBounds
#from ase.ga.startgenerator import StartGenerator
from ase.ga.data import PrepareDB, DataConnection

from gen_stru import gen_V, gen_ase
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
    
def finalize(atoms, calculator, energy=None, forces=None, stress=None):
    # Finalizes the atoms by attaching a SinglePointCalculator
    # and setting the raw score as the negative of the total energy
    print('call finalize ', atoms,flush=True)
    atoms.wrap()
    calc = SinglePointCalculator(atoms, energy=energy, forces=forces,
                                 stress=stress)
    print('call SinglePointCalculator ', atoms,flush=True)
    atoms.calc = calc## use calulator to calcualte the final sing-point energy
    try:
        raw_score = -atoms.get_potential_energy() #
    except:
        raw_score = -1e9
    set_raw_score(atoms, raw_score)
    print('finalize ', atoms, raw_score,flush=True)


def relax(step, atoms, calculator, fitter, cellbounds=None, restart=False):
    # Performs a variable-cell relaxation of the structure
    #calc = EMT()
    #cont = write_vasp("unrelax.vasp", atoms, vasp5=True)
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
    #atoms.set_pbc([True, True, True])
    print('change calculator', calculator, flush=True)
    atoms.calc = calculator
    ##remove WAVECAR for different structures to avoid error
    if os.path.exists('WAVECAR'):
        os.system('rm WAVECAR')

    e = atoms.get_potential_energy()
    #except:
    #    return 1e7
    #print('energy-system:', e, atoms, flush=True)
    f = atoms.get_forces()
    s = atoms.get_stress()
    #print('after relax: ', e)
    finalize(atoms, calculator, energy=e, forces=f, stress=s)
    return e

def ga_run(step, calculator, fitter, cellbounds, name, database='gadb.db', population_size = 20, out=None, rcut=0.5, restart=False ):
# Connect to the database and retrieve some information
    print('cellbounds:', cellbounds)
    if out == None:
        out = 'out' + str(step)
    else:
        out = out + str(step)
    if os.path.exists(out):
        print('rm ' + name + '_' + out + ".xyz")
        os.system('rm ' + name + '_' + out + ".xyz")
        os.system('rm -r ' + out )
    os.system('mkdir ' + out )

    da = DataConnection(database) ##obtain previous results in database
    print('connect database')
    slab = da.get_slab()
    atom_numbers_to_optimize = da.get_atom_numbers_to_optimize()
    n_top = len(atom_numbers_to_optimize)

    f1 = open('GA_step.txt', 'a')
    e_pool = []
    os.system('rm ' + out + '.xyz')
# Use Oganov's fingerprint functions to decide whether
# two structures are identical or not
    comp = OFPComparator(n_top=n_top, dE=1.0,
                     cos_dist_max=1e-3, rcut=10., binwidth=0.05,
                     pbc=[True, True, True], sigma=0.05, nsigma=4,
                     recalculate=False)

# Define the cell and interatomic distance bounds
# that the candidates must obey
    blmin = closest_distances_generator(atom_numbers_to_optimize, rcut)

    cellbounds = CellBounds(bounds=cellbounds)
#    cellbounds = CellBounds(bounds={'phi': [20, 160], 'chi': [20, 160],
#                                'psi': [20, 160], 'a': [2, Lmax],
#                                'b': [2, Lmax], 'c': [2, Lmax]})

# Define a pairing operator with 100% (0%) chance that the first
# (second) parent will be randomly translated, and with each parent
# contributing to at least 15% of the child's scaled coordinates
    pairing = CutAndSplicePairing(slab, n_top, blmin, p1=1., p2=0., minfrac=0.15,
                              number_of_variable_cell_vectors=3,
                              cellbounds=cellbounds, use_tags=False)

# Define a strain mutation with a typical standard deviation of 0.7
# for the strain matrix elements (drawn from a normal distribution)
    strainmut = StrainMutation(blmin, stddev=0.7,cellbounds=cellbounds,
                           number_of_variable_cell_vectors=3,
                           use_tags=False)

# Define a soft mutation; we need to provide a dictionary with
# (typically rather short) minimal interatomic distances which
# is used to determine when to stop displacing the atoms along
# the chosen mode. The minimal and maximal single-atom displacement
# distances (in Angstrom) for a valid mutation are provided via
# the 'bounds' keyword argument.
    blmin_soft = closest_distances_generator(atom_numbers_to_optimize, 0.1) 
    softmut = SoftMutation(blmin_soft, use_tags=False)
# By default, the operator will update a "used_modes.json" file
# after every mutation, listing which modes have been used so far
# for each structure in the database. The mode indices start at 3
# as the three lowest frequency modes are translational modes.

# Set up the relative probabilities for the different operators
   # operators = OperationSelector([4., 3., 3.],
   #                           [pairing, softmut, strainmut])

    operators = OperationSelector([0., 1., 0.],
                             [pairing, softmut, strainmut])
#    print('operator ', operators)    
# Relax the initial candidates
    i = -1
    print('total unrelax configuration', da.get_number_of_unrelaxed_candidates())
    while da.get_number_of_unrelaxed_candidates() > 0:
        a = da.get_an_unrelaxed_candidate()
        i = i + 1
        print('unrelax configuration', i)
        e = relax(step, a, calculator, fitter, cellbounds=cellbounds, restart=restart)
        print('relax energy:', i, e)
        
        e_pool.append(e)
        da.add_relaxed_step(a)
        #try:
        #    da.add_relaxed_step(a)
        #except:
        #    continue

        cell = a.get_cell()
        if not cellbounds.is_within_bounds(cell):
            da.kill_candidate(a.info['confid'])
            print('kill without bounds:', a.cell.cellpar())
        #extxyz.write_xyz(name + '_' + out + ".xyz", a, append=True)
        #cont = write_vasp(out + '/' + name + '_' + str(i) +"_out.vasp", a, vasp5=True)
        #print('epool:', e_pool, min(e_pool))
    #f1.write(format(population_size, '4d') + ' '+ format(min(e_pool), '11.6f') +  '\n')
# Initialize the population
    population = Population(data_connection=da,
                        population_size=population_size,
                        comparator=comp,
                        logfile='log.txt',
                        use_extinct=True)

# Update the scaling volume used in some operators
# based on a number of the best candidates
    current_pop = population.get_current_population()
    strainmut.update_scaling_volume(current_pop, w_adapt=0.5, n_adapt=4)
    pairing.update_scaling_volume(current_pop, w_adapt=0.5, n_adapt=4)

# Test n_to_test new candidates; in this example we need
# only few GA iterations as the global minimum (FCC Ag)
# is very easily found (typically already after relaxation
# of the initial random structures).
    #n_to_test = 50
    i = 0
    while i <= population_size:
        print('Now starting configuration number in GA: {0}'.format(i), ', step:', step, flush=True)

    # Create a new candidate
        a3 = None
        #print('pop',len(population.pop))
        while a3 is None:
            try:
                #print('generate a new structure with GA')
                a1, a2 = population.get_two_candidates()
            except:
                print('fail to generate a new structure with GA ', flush=True)
                continue
            if a1 != None and a2!=None: ##cjl
#                continue
                #pass
                #print('a1, a2:', a1, a2, flush=True)
                try:
                    a3, desc = operators.get_new_individual([a1, a2])
                    print('a3: ', a3, flush=True)
                except:
                    continue
            else:
                print('cannot generate structures from None object')
       
    # Save the unrelaxed candidate
        if i==0:
            os.system('mkdir ' + 'init' + str(step))

        #extxyz.write_xyz('init' + str(step) + ".xyz", a3, append=True) 
        print('write init' + str(step) + '/' + name + '_' + str(i) +".vasp")
        cont = write_vasp('init' + str(step) + '/' + name + '_' + str(i) +".vasp", a3, vasp5=True)

    # Relax the new candidate and save it
        print(f'start relax structure {i} in step {step}' )
        da.add_unrelaxed_candidate(a3, description=desc) # add confid
        e = relax(step, a3, calculator, fitter, cellbounds=cellbounds)
        e_pool.append(e)
        da.add_relaxed_step(a3)
        if e > 1e6:
            continue
        i = i + 1
        #print('finish relax', step)
        #istep = step + population_size + 1 


    # If the relaxation has changed the cell parameters beyond the bounds we
    # disregard it in the population
        cell = a3.get_cell() 
        if not cellbounds.is_within_bounds(cell):
            print('kill', a3.cell.cellpar()) 
            da.kill_candidate(a3.info['confid'])
        else:
            f1.write(format(step, '4d') + ' ' + format(i, '4d') + ' '+ format(min(e_pool), '11.6f') +  '\n')
            extxyz.write_xyz(out + ".xyz", a3, append=True) 
            cont = write_vasp(out + '/' + name + '_' + str(i) +"_out.vasp", a3, vasp5=True)
    # Update the population
        population.update()
        
        #if step % population_size  == 0:
        # Update the scaling volumes of the strain mutation and the pairing
        # operator based on the current best structures contained in the
        # population
    current_pop = population.get_current_population()
    strainmut.update_scaling_volume(current_pop, w_adapt=0.5, n_adapt=4) 
    pairing.update_scaling_volume(current_pop, w_adapt=0.5, n_adapt=4)
    write('current_population.traj', current_pop)
    print('Now finishing configuration number {0}'.format(i))

    #print('GA finished after step %d' % step) 
    hiscore = get_raw_score(current_pop[0]) 
    print('Highest raw score = %8.4f eV' % hiscore)

    all_candidates = da.get_all_relaxed_candidates()
    write('all_candidates.traj', all_candidates) 
    print(len(all_candidates))
    write('all_candidates.xyz', all_candidates, format='xyz')

    current_pop = population.get_current_population()
#    write('current_population.traj', current_pop)

    f1.close()
    np.savetxt(out + '_energy.txt', np.array(e_pool))

def ga_opt(Nstep, ele, Natom, calculator, fitter, cellbounds=None, database='gadb.db', population_size = 20, out=None, rcut=0.5 ):
    name = ''
    for i in range(len(ele)):
        name = name + ele[i] # + str(Natom[i])

    volume = gen_V(ele, Natom, fix=True)
    Lmax = 3*(volume)**(1/3)
    if cellbounds == None:
        cellbounds ={'phi': [20, 160], 'chi': [20, 160],
            'psi': [20, 160], 'a': [2, Lmax],
            'b': [2, Lmax], 'c': [2, Lmax] }

    for i in range(Nstep):
        step = i
        ga_run(step, calculator, fitter, cellbounds, name, population_size = population_size, out=out )

'''
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

os.system('rm ' + database)
print('generate structures')
syss = gen_ase(ele, Natom, volume=None, cellbounds=None, filename=None, N=population_size, rcut=0.5, form='vasp')
print('create database')
ga_create_database(ele, Natom, syss, database=database, relaxed=False)
ga_opt(Nstep, ele, Natom, calculator, fitter, cellbounds=None, database=database, population_size = population_size, out=None, rcut=rcut )
'''
