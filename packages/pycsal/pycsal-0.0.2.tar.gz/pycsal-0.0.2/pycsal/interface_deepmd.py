import dpdata
import numpy as np
import os
import time
#path = 'set0/'

#name = 'Mg4Sn2_out.xyz'
#type_map = ['Mg', 'Sn']

def extxyz_deepmd(name, path, type_map,  UnitE=1, UnitR=1): #mutiple UnitE, UnitR into units eV, A
    #tranform the extxyz format to deepmd raw format
    UnitF = UnitE/UnitR
    print(path)
    if path[-1]!='/':
        path = path + '/'
    if not os.path.exists(name):
        return
    if not os.path.exists(path):
        print('%s not exist' % path )
        os.system('mkdir ' + path)
    if not os.path.getsize(name):
        pass
        #os._exit(0)
    f0 = open(path + 'type_map.raw', 'w')
    #print('type_map: ', type_map)
    for item in type_map:
        #print(item)
        f0.write(item + '\n' )
    f0.close()

    f1 = open(name, 'r')
    f3 = open(path + 'box.raw', 'w')
    f4 = open(path + 'coord.raw', 'w')
    f5 = open(path + 'force.raw', 'w')
    f6 = open(path + 'energy.raw', 'w')
    f7 = open(path + 'type.raw', 'w')

    ip = -1
    while True:
        line = f1.readline()
        if not line:
            break
        ip = ip + 1
        natom = int(line.split()[0])

        line = f1.readline()
        temp = line.split('=')
        for j in range(len(temp)):
            if temp[j].find('energy') > -1:
                ind_ene = j
        #print(temp[ind_ene], temp[ind_ene+1]) 
        temp2 = temp[ind_ene+1].split()

        E = float(temp2[0]) * UnitE
        f6.write(str(E) + '\n')
        
        l1 = line.index('Lattice=')
        l2 = line.index('Properties')
        lat = line[l1+9:l2-2]  
        f3.write(lat + '\n')
        for j in range(natom):
            line = f1.readline()
            temp = line.split()
            F = np.zeros(3)
            coor = np.zeros(3)
            for k in range(3):
                coor[k] = float(temp[k+1]) 
                F[k] = float(temp[k+4]) * UnitF 
            f4.write(str(coor[0]) + ' ' + str(coor[1]) + ' ' + str(coor[2]) + ' ')

            f5.write(str(F[0]) + ' ' + str(F[1]) + ' ' + str(F[2]) + ' ')
            if ip==0:
                for k in range(len(type_map)):
                    if temp[0] == type_map[k]:
                        f7.write(str(k) + '\n')
        f4.write('\n')
        f5.write('\n')
       
    f1.close()
    f3.close()
    f4.close()
    f5.close()
    f6.close()
    f7.close()

    lat = np.loadtxt(path + 'box.raw')
    lat = lat*UnitR
    np.savetxt('box.raw' , lat)


def gen_dpdata(path, nset, test_ratio=0.2): 
    #split raw data into training and valiation sets in npy format
    for i in range(nset+1):
        if not os.path.exists(path + '/set' + str(i) + '/box.raw'):
            continue
        if not os.path.getsize(path + '/set' + str(i) + '/box.raw'):
            continue
        if i == 0:
            data = dpdata.LabeledSystem(path + '/set0', fmt = 'deepmd/raw') 
        else:
            temp = dpdata.LabeledSystem(path + '/set' + str(i), fmt = 'deepmd/raw')
            data.append(temp)
        print('path: %s, set %d:  the data contains %d frames' % (path, i, len(data)) )
    n = len(data)
    # random choose 20% index for validation_data
    n_test = max(1, int(n*test_ratio))
    index_validation = np.random.choice(n,size=n_test,replace=False)
    # other indexes are training_data
    index_training = list(set(range(n))-set(index_validation))
    data_training = data.sub_system(index_training)
    data_validation = data.sub_system(index_validation)
    # all training data put into directory:"training_data"
    data_training.to_deepmd_npy('training_data/' + path)
    # all validation data put into directory:"validation_data"
    data_validation.to_deepmd_npy('validation_data/' + path)
    print('# the training data contains %d frames' % len(data_training))
    print('# the validation data contains %d frames' % len(data_validation))
    return len(data_validation)

def rmse(a, b, cut=[], ncut=[]):
    #calculate the rmse with two factors, ncut contains the number of data in each subsystem
    #cut is the cutoff energy for each subsystem
    c = a-b
    d = []
    ind = np.cumsum(ncut)
    ind = np.insert(ind, 0, 0)
    if len(ncut) > 0:
        for i in range(len(cut)):
            for j in range(ind[i], ind[i+1]):
                if a[i] < cut[i]:
                    d.append(c[i])
        c = np.array(d)
    rmse = np.sqrt( np.mean(c**2) )
    return rmse


def dp_train(step, path='train'):
    #call "dp train" command to start the deepmd training
    cwd = os.getcwd()
    os.chdir(cwd + '/' + path)
    print('start deepmd-kit training', time.gmtime())
    if step == 0:
        os.system('cp input0.json input.json')
        os.system('dp train input.json')
        print('dp train input.json')
    else:
        os.system('cp input1.json input.json')
    
        print('dp train --init-model model.ckpt input.json > fit.log 2>&1')
        os.system('dp train --init-model ' + 'model.ckpt ' + 'input.json >> fit.log ')
    print('finish deepmd-kit training', time.gmtime())

    os.system('dp freeze -o graph.pb')
    #os.system('dp compress -i graph.pb -o graph-compress.pb')
    #os.system('dp test -m graph.pb -s ../validation_data ' + ' -d results ')
    os.chdir(cwd)


def dp_error(cut=[], path='train'):
    #calculate the training error
    cwd = os.getcwd()
    os.chdir(cwd + '/' + path)
    os.system('dp test -m graph.pb -s ../validation_data  -d results  > results.log 2>&1')
    RMSE_set = []
    nval = []
    with open('results.log', 'r' ) as fdp:
        while True:
            line = fdp.readline()
            if not line:
                break
            if line.find('number of test data') > -1:
                nval.append( int(line.split()[-1]) )
            if line.find('Energy RMSE/Natoms') > -1:
                RMSE_set.append( float(line.split()[-2]) )
            if line.find('weighted average of errors') > -1:
                break
    if len(nval)!=len(RMSE_set):
        print('inconsisitent of RMSE and number of sets!!!', nval, RMSE_set)
    
    if len(cut)!=len(nval):
        print('inconsisitent of cutoffs and number of sets!!!', cut)
    
    os.chdir(cwd)
    ene = np.loadtxt(path + '/results.e_peratom.out')
    rmse_et = rmse(ene[:, 0], ene[:, 1])
    if len(cut)!=0:
        rmse_ec = rmse(ene[:, 0], ene[:, 1], cut=cut, ncut=nval)#RMSE excluding data wiht energy higher than cut value
    else:
        rmse_ec = -1
    force = np.loadtxt(path + '/results.f.out')
    rmse_f = rmse(force[:, 0], force[:, 1])
    viral = np.loadtxt(path + '/results.v_peratom.out')
    rmse_v = rmse(viral[:, 0], viral[:, 1])
    
    return [rmse_et, rmse_ec, rmse_f, rmse_v, RMSE_set]
