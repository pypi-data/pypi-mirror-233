import numpy as np
from random import random
import os 
import torch
def extxyz_reann(name, ratio=0.8, UnitE=1, UnitR=1):
#mass = {'Mg':24.305, 'Sn':118.69}
    UnitF = UnitE/UnitR
    atom2mass={ 'H':1.008,     'He':4.003,   'Li':6.941,    'Be':9.012,   'B':10.811,     'C':12.017,     'N':14.007,     'O':15.999,
             'F':18.998,     'Ne':20.180,  'Na':22.990,   'Mg':24.305,  'Al':26.982,   'Si':28.086,   'P':30.974,    'S':32.065,
             'Cl':35.453,   'Ar':39.948,  'K':39.098 ,    'Ca':40.078,  'Sc':44.956,   'Ti':47.867,   'V':50.942,    'Cr':51.996,
             'Mn':54.938,   'Fe':55.845,  'Co':58.933,   'Ni':58.693,  'Cu':63.546,   'Zn':65.409,   'Ga':69.723,   'Ge':72.64,
             'As':74.922,   'Se':78.96,  'Br':79.904,   'Kr':83.798,  'Rb':85.467,   'Sr':87.62,   'Y':88.906,    'Zr':91.224,
             'Nb':92.907,   'Mo':95.94,  'Tc':97.907,   'Ru':101.07,  'Rh':102.905,   'Pd':106.42,   'Ag':107.868,   'Cd':112.411,
             'In':114.818,   'Sn':118.710,  'Sb':121.760,   'Te':127.60,  'I':126.904,    'Xe':131.293,   'Cs':132.905,   'Ba':137.327,
             'La':138.905,   'Ce':140.116,  'Pr':140.908,   'Nd':144.242,  'Pm':145,   'Sm':150.36,   'Eu':151.964,   'Gd':157.25,
             'Tb':158.925,   'Dy':162.500,  'Ho':164.930,   'Er':164.930,  'Tm':168.934,   'Yb':173.04,   'Lu':174.967,   'Hf':178.49,
             'Ta':180.948,   'W':183.84,   'Re':186.207,   'Os':190.23,  'Ir':192.217,   'Pt':195.084,   'Au':196.967,   'Hg':200.59,
             'Tl':204.383,   'Pb':207.2,  'Bi':208.980,   'Po':208.982,  'At':209.987,   'Rn':222.018,   'Fr':223,   'Ra':226,
             'Ac':227,   'Th':232.038,  'Pa':231.036,   'U':238.029,   'Np':237,   'Pu':244,   'Am':243,   'Cm':247,
             'Bk':247,   'Cf':251,  'Es':252,   'Fm':257, 'Md':258,  'No':259,  'Lr':262,  'Rf':261,
             'Db':262,  'Sg':266, 'Bh':264,  'Hs':277, 'Mt':268,  'Ds':281,  'Rg':272,  'Cn':285,
             'Uut':284, 'Fl':289, 'Uup':288, 'Lv':293, 'Uus':291, 'UUo':294}
    f1 = open( name + '.xyz', 'r')
    f2 = open(name + '.dat', 'w')
    f3 = open(name + '_train.configuration', 'w')
    f4 = open(name + '_test.configuration', 'w')

    ip = -1
    it = -1
    iv = -1
    while True:
        line = f1.readline()
        if not line:
            break
        ip = ip + 1
        f2.write('point= ' + str(ip) + '\n')
        natom = int(line.split()[0])
        line = f1.readline()
        temp = line.split('=')   
        temp2 = temp[-2].split()
    #    f2.write(temp2[0] + '\n')
        E = float(temp2[0]) * UnitE

        
        l1 = line.index('Lattice=')
        l2 = line.index('Properties')
        lat = line[l1+9:l2-2]
        lat = lat.split()
        for k in range(3):
            f2.write(lat[3*k] + ' ' + lat[3*k+1] + ' ' + lat[3*k+2] + '\n')
        f2.write('pbc 1 1 1 \n')
        
        seed = random()
        if seed < ratio:
            it = it + 1
            f3.write('point= ' + str(it) + '\n')
            for k in range(3):
                f3.write(lat[3*k] + ' ' + lat[3*k+1] + ' ' + lat[3*k+2] + '\n')
            f3.write('pbc 1 1 1 \n')
        else:
            iv = iv + 1
            f4.write('point= ' + str(iv) + '\n')        
            for k in range(3):
                f4.write(lat[3*k] + ' ' + lat[3*k+1] + ' ' + lat[3*k+2] + '\n')
            f4.write('pbc 1 1 1 \n')
                
        for j in range(natom):
            line = f1.readline()
            temp = line.split()
            F = np.zeros(3)
            coor = np.zeros(3)
            for k in range(3):
                coor[k] = float(temp[k+1])
                F[k] = float(temp[k+4]) * UnitF 
            scoor = str(coor[0]) + ' ' + str(coor[1]) + ' ' + str(coor[2]) + ' '
            sforce = str(F[0]) + ' ' + str(F[1]) + ' ' + str(F[2]) + ' '
            imass = str(atom2mass[temp[0]])
            f2.write(temp[0] + ' ' +  imass + ' ' + scoor + sforce + '\n')
            if seed < ratio:
                f3.write(temp[0] + ' ' +  imass + ' ' + scoor + sforce + '\n')
            else:
                f4.write(temp[0] + ' ' +  imass + ' ' + scoor + sforce + '\n')            
        f2.write('abprop: ' + str(E) + '\n')
        if seed < ratio:
            f3.write('abprop: ' + str(E) + '\n')
        else:
            f4.write('abprop: ' + str(E) + '\n')     

        
    f1.close()
    f2.close()
    f3.close()
    f4.close()

def reann_data(prefix, step,  path='reann_train', ratio=0.8, UnitE=1, UnitR=1):
    if not os.path.exists(path + '/train'):
        os.system('mkdir ' + path + '/train')
    if not os.path.exists(path + '/test'):
        os.system('mkdir ' + path + '/test')

    for i in range(step+1):
        if i==0:
            os.system('cat ' + prefix + str(i) + '.xyz> pick.xyz')
        else:
            os.system('cat ' + prefix  + str(i) + '.xyz>> pick.xyz')
    extxyz_reann(prefix)
    os.system('cp ' + prefix  + '_train.configuration ' + path + '/train/configuration')
    os.system('cp ' + prefix  + '_test.configuration ' + path + '/test/configuration')

        
def reann_train(step, reann_exe, path='reann_train'):

    cwd = os.getcwd()
    os.chdir(cwd + '/' + path)
    if step == 0:
        os.system('cp input0_nn ./para/input_nn')
    else:
        os.system('cp input1_nn ./para/input_nn')
    os.system(reann_exe )
    os.chdir(cwd)

def RMSE(a, b, cut=[], ncut=[]):
    #print(type(a),type(np.array(a)),a)
    a=np.array(a)
    b=np.array(b)
    c = np.array(a)-np.array(b)
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

def gpu_sel():
    os.system('nvidia-smi -q -d Memory |grep -A4 GPU|grep Free >gpu_info')
    memory_gpu=[int(x.split()[2]) for x in open('gpu_info','r').readlines()]
    if memory_gpu:
       gpu_queue=sorted(range(len(memory_gpu)), key=lambda k: memory_gpu[k],reverse=True)
       str_queue=""
       for i in gpu_queue:
           str_queue+=str(i)
           str_queue+=", "
       os.environ['CUDA_VISIBLE_DEVICES']=str_queue
    os.system('rm gpu_info')
#extxyz_reann('B12_pick0')   

def reann_error(atomtype, cut=[], ncut=[], path='reann_train', model='REANN_PES_DOUBLE.pt'):
    cwd = os.getcwd()
    os.chdir(cwd + '/' + path)
# used for select a unoccupied GPU
    gpu_sel()
# gpu/cpu
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# same as the atomtype in the file input_density
#atomtype=["O","H"]
#load the serilizable model
    pes=torch.jit.load(model)
# FLOAT: torch.float32; DOUBLE:torch.double for using float/double in inference
    pes.to(device).to(torch.double)
# set the eval mode
    pes.eval()
    pes=torch.jit.optimize_for_inference(pes)
# save the lattic parameters
    cell=np.zeros((3,3),dtype=np.float64)
    period_table=torch.tensor([1,1,1],dtype=torch.double,device=device)   # same as the pbc in the periodic boundary condition
    npoint=0
    #rmse=torch.zeros(2,dtype=torch.double,device=device)
    e0=[]
    ep=[]
    f0=[]
    fp=[]
    rmse_f = 0 
    with open("test/configuration",'r') as f1:
        while True:
            string=f1.readline()
            if not string: break
            string=f1.readline()
            cell[0]=np.array(list(map(float,string.split())))
            string=f1.readline()
            cell[1]=np.array(list(map(float,string.split())))
            string=f1.readline()
            cell[2]=np.array(list(map(float,string.split())))
            string=f1.readline()
            species=[]
            cart=[]
            abforce=[]
            mass=[]
            while True:
                string=f1.readline()
                if "abprop" in string:
                    abprop = float(string.split()[1])
                    npoint = npoint + 1
                    break
                tmp=string.split()
                tmp1=list(map(float,tmp[2:8]))
                cart.append(tmp1[0:3])
                abforce.append(tmp1[3:6])
                mass.append(float(tmp[1]))
                species.append(atomtype.index(tmp[0]))
            abene=float(string.split()[1])
            abene=torch.from_numpy(np.array([abene])).to(device)
            species=torch.from_numpy(np.array(species)).to(device)  # from numpy array to torch tensor
            cart=torch.from_numpy(np.array(cart)).to(device).to(torch.double)  # also float32/double
            mass=torch.from_numpy(np.array(mass)).to(device).to(torch.double)  # also float32/double
            abforce=torch.from_numpy(np.array(abforce)).to(device).to(torch.double)  # also float32/double
            tcell=torch.from_numpy(cell).to(device).to(torch.double)  # also float32/double
            energy,force=pes(period_table,cart,tcell,species,mass)
            energy=energy.detach().cpu()
        #print(energy)
            force=force.detach().cpu().numpy()
            na = len(species)
            abforce = np.array(abforce.cpu())
            print(na)
            e0.append(abprop); ep.append(energy.numpy() )
            f0.append(abforce); fp.append(force)
            #rmse[0] = rmse[0] + ((abprop-energy)/na)**2
            rmse_f = rmse_f + np.sum((force - abforce)*(force - abforce))/3/na
    print(ep )  
#    e0 = e0.detach().cpu().numpy()
#    ep = ep.detach().cpu().numpy()
    rmse_et = RMSE(e0, ep)
    if len(cut)!=0:
#cut is the cutoff for each set while ncut is the number of each set
        rmse_ec = RMSE(e0, ep, cut=cut, ncut=nval)#RMSE excluding data wiht energy higher than cut value
    else:
        rmse_ec = -1

    #rmse = np.sqrt(rmse.cpu()/npoint)
    os.chdir(cwd)
    #print(na,npoint,rmse)
    rmse_v = 0
    return [rmse_et, rmse_ec, rmse_f, rmse_v]

#reann_data('pick', 19)
#extxyz_reann('pick', path='reann_train', ratio=0.8, UnitE=1, UnitR=1)
#import torch
#reann_train(0)
#reann_error(['P'], path='reann_train', model='REANN_PES_DOUBLE.pt')

