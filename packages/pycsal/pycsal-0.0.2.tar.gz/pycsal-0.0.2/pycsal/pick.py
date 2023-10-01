from ase import Atom, Atoms
from ase.calculators.lammpslib import LAMMPSlib
from ase.io import read, write, extxyz
from ase.io.vasp import read_vasp, write_vasp, write_vasp_xdatcar
from ase.constraints import ExpCellFilter
from ase.optimize import BFGS,FIRE, BFGSLineSearch
import os
import numpy as np
from gen_stru import check, gen_V

def pick(inp, out, step, nsys, name,  calculator, fitter , Ecut=0, rcut=0.5, form='vasp', flag_val=False):
    if form != '.xyz' and not os.path.exists(inp):
        print('input path not exist: ', inp)
        #os._exit(0)

    f1 = open(out + '_info.dat', 'w')
    f2 = open(out + '.dat', 'w')
    if os.path.exists(out + ".xyz"):
        os.system('rm ' +  out + ".xyz")
    print('rm '  + out + ".xyz")
    
    count = 0
    error_e = []
    error_f = []

    syss = []
    if form == 'xyz':
        print('read ' + inp  + '.' + form)
        syss = read( filename=  inp  + '.' + form , index=':', format='extxyz')
    else:
        if step == 0:
            file_list = os.listdir(inp)
            nsys = len(file_list)

        for i in range(0, nsys):
            if not os.path.exists(inp + '/' + name + '_' + str(i) + '_out.' + form):
                continue
            sys = read( filename= inp + '/' + name + '_' + str(i) + '_out.' + form, format=form)
            syss.append(sys)
            print(inp + '/' + name + '_' + str(i) + '_out.' + form)
        syss.append(sys)
#    print(len(syss))
    ncount = 0
    for sys in syss:
        ncount = ncount+1
#        sys.set_pbc('T T T')
#        print(sys)
    #    print(out)
        ele = sys.get_chemical_symbols(); natom = np.ones(len(ele))
        compo = sys.get_chemical_formula()
        V0 = gen_V(ele, natom, fix=True)
        vol = sys.get_volume()
        if vol > 1.5*V0 and step > 0:
            continue
        #rc = min(0.1+0.2*step , rcut)
        rc = rcut
        #print('check')
        if len(natom) > 1:
            if check(sys, rc) == False:
            #print(compo, 'small interatomic distance')
                continue
        

        if flag_val == False:
            extxyz.write_xyz(out + ".xyz", sys, append=True)
            count = count+1
            continue

        #count = count+1
        sys.calc = calculator#fitter #calculator
        vol = sys.get_volume()
        cell = sys.cell.cellpar()
        energy = sys.get_potential_energy()
        forces = sys.get_forces()

        if energy > Ecut:
            print('high-energy: ', compo, energy)
            continue
        count = count+1
        extxyz.write_xyz(out + ".xyz", sys, append=True)

        if step > 0 :
            sys0 = sys
            sys0.calc = fitter
            e0 = sys0.get_potential_energy()
            f0 = sys0.get_forces()
            print('e_true vs e_pred:', e0 , energy, flush=True)
            f2.write(str(e0) + ' ' + str(energy) + '\n')
            error_e.append( (e0 - energy)/len(sys0) )
            error_f.append(np.mean((forces-f0)**2))
            
        f1.write( format(count, '<6d') + ' ')
        f1.write(format(energy, '>10.5f') + ' ')
        f1.write(format(vol, '>10.3f') + ' ')
        for j in range(6):
            f1.write(format(cell[j], '>7.2f') + ' ')
        f1.write('\n')
    #    cont = write_vasp(out + '/' + name + str(i) +"_out.vasp", sys, vasp5=True)
    #    extxyz.write_xyz(name + out + ".xyz", sys, append=True)

    f1.close()
    f2.close()
    #extxyz_deepmd(name+ out + ".xyz", "set"+ str(step), ['Mg', 'Sn'])
    print("pick %d from %d" %(count, ncount))
    if count == 0 or step == 0 or flag_val==False:
        RMSE_E  = -1
        RMSE_F = -1
    else:
        RMSE_E = np.sqrt(np.mean(np.array(error_e)**2))
        RMSE_F = np.sqrt(np.mean(error_f))
    return count, RMSE_E, RMSE_F

