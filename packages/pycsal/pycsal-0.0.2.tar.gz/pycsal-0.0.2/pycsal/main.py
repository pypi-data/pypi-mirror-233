import os
print(os.system(' which python'))
#os.system(f'source ~/.bashrc')
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
from ga import ga_opt, ga_create_database, ga_run
import yaml
from init import read_input
import numpy as np

var = read_input()
globals().update(var)
if potential == 'deepmd':
    train_path = 'train'
    from interface_deepmd import extxyz_deepmd, gen_dpdata, dp_error, dp_train
elif potential == 'reann':
    train_path = 'reann_train'
    from interface_reann import extxyz_reann, reann_data, reann_error, reann_train

#os._exit(0)
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
        gen(init, inp, ele, Natom_list, nsys, name, system_weight, Natom_weight=Natom_weight, cellbounds=cellbounds, rcut=rcut, spg=spg)
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
