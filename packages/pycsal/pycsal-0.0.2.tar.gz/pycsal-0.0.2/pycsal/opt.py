from ase import Atom, Atoms
from ase.build import bulk
#from ase.calculators.lammpsrun import LAMMPS
#from ase.calculators.lammpslib import LAMMPSlib
from ase.optimize import BFGS,FIRE,GPMin, BFGSLineSearch
from ase.optimize.sciopt import SciPyFminBFGS, SciPyFminCG
from ase.io import read, write, extxyz
from ase.io.vasp import read_vasp, write_vasp, write_vasp_xdatcar
from ase.constraints import ExpCellFilter
#from deepmd.calculator import DP
import os
import numpy as np
def opt(inp, out, step, nsys, name, calculator, fitter, fconv=0.05,train_path='train', start_opt=0, optimizer='BFGS'):
    syss = []
    if not os.path.exists(inp):
        print('input files not exist')
    #    os._exit(0)
    print('start optimization from ', start_opt )
    if start_opt == 0:
        print('rm ' +  out + ".xyz")
        os.system('rm '  + out + ".xyz")
        os.system('rm -r ' + out )
    if not os.path.exists(out):
        os.system('mkdir ' + out )
    print('write to ' + name + '_' + out + ".xyz", flush=True)
    f1 = open(out  + '_info.dat', 'w')
    for i in range(start_opt, nsys):
        #print(type(calculator))
        if os.path.exists('WAVECAR'):
            os.system('rm WAVECAR')
        #if os.path.exists('vasprun.xml'):
        #    os.system('rm vasprun.xml')
        #if os.path.exists('OUTCAR'):
        #    os.system('rm OUTCAR')

        if out == 'final':
            sys = read( filename= inp + '/' + name + '_' + str(i) + '_out.vasp', format='vasp')
        else:
            if not os.path.exists(inp + '/' + name + '_' + str(i) + '.vasp'):
                continue
            sys = read( filename= inp + '/' + name + '_' + str(i) + '.vasp', format='vasp')
            print( inp + '/' + name + '_' + str(i) + '.vasp')
        if step == 0:
            sys.calc = calculator
            fconv = 0.01
            #extxyz.write_xyz(name + out + ".xyz", sys, append=True)
            #cont = write_vasp(out + '/' + name + str(i+5*nsys) +"_out.vasp", sys, vasp5=True)
        else:
            sys.calc = fitter
            fconv = fconv
        print(sys, flush=True) #,sys.numbers.argsort(order=['Ti', 'O']))
        #print('using ' + optimizer, sys.calc)
        sys = ExpCellFilter(sys)
        try:
            sys.get_forces()    
        except:
            continue
        #print('using ' + optimizer)
        if optimizer == 'GPMin':
            dyn = GPMin(atoms= sys, logfile='opt.log')
        if optimizer == 'BFGS':
            dyn = BFGS(atoms= sys, logfile='opt.log')
        if optimizer == 'FIRE':
            dyn = FIRE(atoms= sys, logfile='opt.log')
        if step == 0:   
            try:
                conv = dyn.run(fmax=1.0, steps=200)
            except:
                continue
            if conv == False:
                continue
            fmax = np.max(sys.get_forces())
            sys0 = sys.atoms
            extxyz.write_xyz( out + ".xyz", sys0, append=True)
            cont = write_vasp(out + '/' + name + '_' + str(i+nsys) +"_out.vasp", sys0, vasp5=True)
            print('fmax: ', fmax, flush=True)
            if fmax>0.5:
                try:
                    dyn.run(fmax=0.5, steps=200)
                except:
                    continue
                fmax = np.max(sys.get_forces())
                sys0 = sys.atoms
                
                #extxyz.write_xyz( out + ".xyz", sys0, append=True)
                #cont = write_vasp(out + '/' + name + '_' + str(i+2*nsys) +"_out.vasp", sys0, vasp5=True)
            if fmax > 0.3:
                try:
                    dyn.run(fmax=0.3, steps=200)
                except:
                    continue
                fmax = np.max(sys.get_forces())
                sys0 = sys.atoms
                #extxyz.write_xyz(out + ".xyz", sys0, append=True)
                #cont = write_vasp(out + '/' + name + '_' + str(i+3*nsys) +"_out.vasp", sys0, vasp5=True)
            if fmax > 0.1:
                try:
                    dyn.run(fmax=0.1, steps=200)
                except:
                    continue
                fmax = np.max(sys.get_forces())
                sys0 = sys.atoms
                extxyz.write_xyz(out + ".xyz", sys0, append=True)
                cont = write_vasp(out + '/' + name + '_' + str(i+4*nsys) +"_out.vasp", sys0, vasp5=True)

        #dyn = BFGSLineSearch(atoms= sys, logfile='opt.log')
        #dyn.run(fmax=fconv, steps=100)
        if optimizer == 'GPMin':
            dyn = GPMin(atoms= sys, logfile='opt.log')
        if optimizer == 'BFGS':
            dyn = BFGS(atoms= sys, logfile='opt.log')
        try:
            conv =dyn.run(fmax=fconv, steps=200)
        except:
            continue
        forces = sys.get_forces()
        if np.max(forces) > 20:
            continue 
        dyn = FIRE(atoms= sys, logfile='opt.log')
        try:
            conv =dyn.run(fmax=fconv, steps=200)
        except:
            continue
        dyn = BFGS(atoms= sys, logfile='opt.log')
        try:
            conv = dyn.run(fmax=fconv, steps=200)
        except:
            continue
        if conv == False:
            continue
        sys = sys.atoms
        syss.append(sys)
        vol = sys.get_volume()
        cell = sys.cell.cellpar()
        energy = sys.get_potential_energy()
        #print(energy, cell)
        f1.write( format(i, '<6d') + ' ')
        f1.write( format(i, '<6d') + ' ')
        f1.write(format(sys.get_chemical_formula(), '6s') + ' ')
        f1.write(format(vol, '>10.3f') + ' ')
        for j in range(6):
            f1.write(format(cell[j], '>7.2f') + ' ')
        f1.write('\n')
        cont = write_vasp(out + '/' + name + '_' + str(i) +"_out.vasp", sys, vasp5=True)
        extxyz.write_xyz( out + ".xyz", sys, append=True)
    f1.close()
    return syss


