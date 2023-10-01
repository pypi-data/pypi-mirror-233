import yaml
import numpy as np
from gen_stru import gen_V
import os
def read_input(input_search = 'search.yaml'):
    try:
        import psutil
        #nprocess = psutil.cpu_count()
        nprocess = len(psutil.Process().cpu_affinity()) #get the number of available cpu cores
        print('available cpu cores is', nprocess )
    except:
        nprocess = 1
    ninit= 20
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
    population_size = 20
    switch_ga = 1e7
    database = 'gadb.db'
    rLJ = 6.0
    sigma = 1.0
    ##------------------------------------------
    with open(input_search) as f:
        x = yaml.safe_load(f)
    globals().update(x)
    #for key,val in x.items():
     #   exec(key + '=val')
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

    if calculation=='lammps':
        from ase.calculators.lammpslib import LAMMPSlib
        lammps = LAMMPSlib(lmpcmds=cmds, logfile='test.log', keep_alive = True )
        calculator = lammps
    
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
            from ase.calculators.vasp import Vasp
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
    #print(locals())
    #print(globals())
    var1 = locals()
    var2 = globals()
    var = var1 | var2
    #var = var1
    #print(var)
    keys = list(var.keys())
    for key in keys:
        #key = keys[i]
        item = var[key]
        if key == None or key == 'calculator':
            continue
        
        try:
            if str(item).find('module') > -1 or str(item).find('function') > -1 :
                var.pop(key)
            elif str(item).find('class') > -1 or str(item).find('object') > -1 :
                var.pop(key)
            elif key.find('__') > -1 or str(item).find('io.') > -1 :
                var.pop(key)                
        except:
            print('no',key, item)
    #var = globals()
    print(var)
    return var
#read_input()
