import numpy as np
import os
from ase.io import read
from opt import opt
from gen_stru import gen, gen_V
from pick import pick
#from interface_deepmd import extxyz_deepmd, gen_dpdata, dp_error, dp_train
#from interface_reann import extxyz_reann, reann_data, reann_error, reann_train 
#from deepmd.calculator import DP
#from reann import REANN
from tool import get_xyz_frames,split_xyz, delete_xyz_frames 
from  PCM import asap_pcm
#from ase.calculators.lammpslib import LAMMPSlib
from ase.calculators.vasp import Vasp
from ga import ga_opt, ga_create_database, ga_run
import yaml
import time

class search():
    def __init__(self, **kwargs):           
        try:
            import psutil
            #nprocess = psutil.cpu_count()
            nprocess = len(psutil.Process().cpu_affinity()) #get the number of available cpu cores
            print('available cpu cores is', nprocess )
        except:
            nprocess = 1
        ninit = 20
        niter = 40
        sstep = 0
        nstep = 20 
        keep_ratio = 0.5
        Ecut = 1.0 # energy above formation energy per atom
        rcut = 0.7
        system_weight = [1,1,1,1,0,0,0] ##weight for 7 crystal systems
        Econv = 0.005  ### fitter RMES < EconV eV , stop
        Natom_weight = []
        spg = None
        regen = 1
        start_opt = 0
        optimizer = 'BFGS'
        #nprocess = 1
        ASE_VASP = False
        ##default parameters for genetic algorithm
        switch_ga = 1e7
        database = 'gadb.db'
        population_size = 20
        rLJ = 6.0
        sigma = 1.0
    ##------------------------------------------
    with open('search.yaml') as f:
        x = yaml.safe_load(f)
    globals().update(x)
    if len(Natom_list) > 1:
        print('cannot using genetic algorithm with multiple combinations')
        os._exit(0)
    else:
        Natom = Natom_list[0]
    if start_opt > 0:
        regen = 0
    if "E0" not in dir():
        E0 = np.zeros(len(ele))
    #print(dir())
    if 'cellbounds' not in dir():
        cellbounds = {'phi': [20, 160], 'chi': [20, 160], 'psi': [20, 160], 'a': [1, 5], 'b': [1, 5], 'c': [1, 5] }
    volume = gen_V(ele, Natom_list[0])
    Lmax = 3*(volume)**(1/3)
    cellbounds['a'][1] = Lmax; cellbounds['b'][1] = Lmax; cellbounds['c'][1] = Lmax;
    ####--------------------------
    if potential == 'deepmd':
        train_path = 'train'
        from interface_deepmd import extxyz_deepmd, gen_dpdata, dp_error, dp_train
    elif potential == 'reann':
        train_path = 'reann_train'
        from interface_reann import extxyz_reann, reann_data, reann_error, reann_train

    if calculation=='lammps':
        from ase.calculators.lammpslib import LAMMPSlib
        lammps = LAMMPSlib(lmpcmds=cmds, logfile='test.log', keep_alive = True )
        calculator = lammps
        print(globals())
    elif calculation == 'LJ':
        from ase.calculators.lj import LennardJones
        calculator = LennardJones(sigma=sigma, rc=rLJ, smooth=True)

    elif calculation=='vasp':
        from vasp_interactive import VaspInteractive
        nprocess = 1
        command = 'vasp_std'
        xc='PBE'
    #    encut = 350.0 #PW cut-off 
        ispin=1 #No spin-polarization 
        kpts = [1,1,1]
        sigma=0.05
        potim=0.0
        isym=0
        ismear = 0
        algo='fast'
        with open(calculation+'.yaml') as f:
            para_vasp = yaml.safe_load(f)
        globals().update(para_vasp)

        if 'nprocess' in dir():
            for nc in range(1, int(np.sqrt(nprocess))+1 ):
                if nprocess % nc == 0:
                    ncore = nc
    #    if command.find('gam') > -1:
    #        ncore = 1
        print(globals())
        if ASE_VASP == True:
            calculator = Vasp(command='mpirun -np ' + str(nprocess) + ' ' + command,
                            xc=xc,
                            encut = encut, #PW cut-off
                            ispin=ispin, #No spin-polarization
                            kpts = kpts,
                            sigma=sigma,
                            potim=potim,
                            isym=isym,
                            ismear = ismear,
                            algo=algo,
                            ncore=ncore #Band parallezation use kpar for k-points
                            )
        else:
            calculator = VaspInteractive(command='mpirun -np ' + str(nprocess) + ' ' + command,
                            xc=xc,
                            encut = encut, #PW cut-off
                            ispin=ispin, #No spin-polarization
                            kpts = kpts,
                            sigma=sigma,
                            potim=potim,
                            isym=isym,
                            ismear = ismear,
                            algo=algo,
                            ncore=ncore, #Band parallezation use kpar for k-points
                            allow_restart_process=True
                            )

    else:
        print('Wrong parameter name for setting a calculator')
        os._exit(0)

count = 0
name = ''
for i in range(len(ele)):
    name = name + ele[i]
#name = name + '_'
formulars = []
Ef0 = np.zeros(len(Natom_list))
for i in range(len(Natom_list)):
    temp = ''
    for j in range(len(ele)):
        Ef0[i] = Ef0[i] + E0[j]*Natom_list[i][j]
        if Natom_list[i][j]==1:
            temp = temp + ele[j]
        else:
            temp = temp + ele[j] + str(Natom_list[i][j])
    formulars.append(temp)
    Ef0[i] = Ef0[i]/np.sum(Natom_list[i])
    os.system('mkdir ' + temp)
print('formulars: ', formulars)
f1 = open(name + '_' + 'RMSE.log', 'a')
#f1.write('#Ecut = ' + str(Ecut) + ' eV\n')
#f2 = open(name + 'RMSE.log', 'a')
for step in range(sstep, nstep+1):
    inp = 'init' + str(step)
    out = 'out' + str(step)
    if step > 0:
#        fitter = calculator      
        if potential == 'deepmd':
            from deepmd.calculator import DP
            fitter = DP(model= train_path + "/graph.pb")
        if potential == 'reann':
            from reann import REANN
            import torch
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            device = 'cpu'
            fitter = REANN(device=device, atomtype=ele, period='1 1 1', nn = train_path + '/REANN_PES_DOUBLE.pt')
        nsys = niter
    else:
        fitter = calculator
        nsys = ninit
    if regen == 0:
        regen = 1
    if regen == 1 and step < switch_ga:
        gen(inp, ele, Natom_list, nsys, name, system_weight, Natom_weight=Natom_weight, cellbounds=cellbounds, rcut=rcut, spg=spg)
    print("start optimziation step %d" %(step))
#    os._exit(0)
    if step < switch_ga: 
        syss = opt(inp, out, step, nsys, name, calculator, fitter, train_path='train', start_opt=start_opt, optimizer=optimizer)
        if start_opt!=0:
            start_opt = 0
            #print(syss)
    if step == switch_ga:
        if 'syss' not in dir():
            print('read ' + 'pick' + str(step-1) + '.xyz')
            syss = read( filename= 'pick' + str(step-1) + '.xyz', index=':', format='extxyz')
        if os.path.exists(database):
            os.system('rm ' + database)
        print('create database')
        print('ga_run name:', name)
        print('create database', len(syss))
        ga_create_database(ele, Natom, syss, database=database, relaxed=False)
        ga_run(step, calculator, fitter, cellbounds, name, database=database, population_size = population_size, out=None, restart = True )
    elif step > switch_ga:
        ga_run(step, calculator, fitter, cellbounds, name, database=database, population_size = population_size, out=None )    
    #os._exit(0)
    print("finish optimziation step %d" %(step), flush=True)
### pick and re-train

    fpick = 'pick' + str(step)
    #out = name  + '_' + out 
    #if step == 0:
        
    dcount, RMSE_E, RMSE_F = pick(out, fpick, step, nsys, name, calculator, fitter, Ecut=Ecut,rcut=rcut, form='xyz', flag_val=False)
    print('RMSE: %f %f in step %d' %(RMSE_E, RMSE_F, step), flush=True)
#    if step == nstep and step > 0:
#        break
    if step == 0:
        split_xyz(fpick + '.xyz', fpick)
        for formular in formulars:
            if potential == 'deepmd':
                extxyz_deepmd(formular  + "_pick0.xyz", formular + "/set"+ str(0), ele)
    else:
        ncount = get_xyz_frames('pick' + str(step) + '.xyz')
        Di = asap_pcm('pick' + str(step) + '.xyz', n_process=nprocess)
        for istep in range(0, step+1):
            if istep == 0:
                string = '>'
            else:
                string = '>>'
            os.system('cat pick' + str(istep)  + '.xyz' + string + 'temp.xyz') 
            print('cat pick' + str(istep) + '.xyz' + string + 'temp.xyz')
        Dt = asap_pcm('temp.xyz', n_process=nprocess)
        score = Di + np.append(Dt[-1*ncount:-1], Dt[-1])
        rank = sorted(score, reverse = True)
        scut = rank[int(ncount*keep_ratio)]
        flag = np.where(score>=scut, True, False) 
        #nkeep = min(int(ncount*keep_ratio), max_keep)
        #out_soap = 'asap_soap'
        #asap_select('pick', out_soap+str(step), step, nkeep)
        #split_xyz('pick' + str(step) + '.xyz', 'pick' + str(step), flag)
        delete_xyz_frames(infile=fpick+'.xyz', outfile=fpick+'_0.xyz', delete_id = flag)

        count, RMSE_E, RMSE_F = pick(fpick+'_0', fpick, step, nsys, name, calculator, fitter, rcut=rcut, form='xyz', flag_val=True)
        if count == 0:
            print('cannot pick structures from structures searched by GA')
            os._exit(0)
        os.system('cat ' + str(step) + '_' + str(count) + '>> cost.dat')
        split_xyz(fpick + '.xyz', fpick)
        f1.write(format(step, '3d') + ' ')
        f1.write(format(RMSE_E, '8.3f') + ' ')
        f1.write(format(RMSE_F, '8.3f') + ' ')
        print(formulars)

        for formular in formulars:
            print(formular + '_' + fpick + '.xyz')
            if potential == 'deepmd':
                print(formular + '_' + fpick + '.xyz', formular + "/set"+ str(step), ele)
                extxyz_deepmd(formular + '_' + fpick + '.xyz', formular + "/set"+ str(step), ele)
            if potential == 'reann':
                extxyz_reann(formular + '_' + fpick + '.xyz')
    #count = count + dcount
    '''
    if RMSE_E >= 0 and RMSE_E < Econv:
        print('reach the convergence RMSE :%f in step %d' %(RMSE_E, step))
        break

    if count < 0:
        print('effective %d in step %d ' %(count, step))
        nsys= nsys*2 #increase sampling
    else:
        count = 0
    '''
    if potential == 'deepmd':
        nval = []
        for formular in formulars: 
            nval.append( gen_dpdata(formular, step) )
        #os._exit(0)
#        print('start deepmd-kit training', time.gmtime())
        dp_train(step)

        RMSE_fit = dp_error(Ef0 + Ecut)
        Natom_weight = RMSE_fit[-1]
        print("finish training step %d" % step, Natom_weight)

 
        for j in range( len(RMSE_fit)-1):
            f1.write(format(RMSE_fit[j], '8.3f') + ' ')  
        f1.write('\n')
    if potential == 'reann':
        reann_data(prefix= 'pick', step=step)
        reann_train(step=step, reann_exe=reann_exe)
        RMSE_fit = reann_error(ele, path='reann_train', model='REANN_PES_DOUBLE.pt')
f1.close()
