from random import random, uniform, choices, randint, sample
import numpy as np
from math import cos, sin, sqrt, pi
from ase.geometry import get_distances
from ase import Atoms, geometry
from ase.io import read, write, extxyz
from mendeleev.fetch import fetch_table
import pandas as pd
import os

from ase.data import atomic_numbers
from ase.ga.utilities import closest_distances_generator, CellBounds
from ase.ga.startgenerator import StartGenerator

from gen_randSpg import randSpg
### some constants
NA = 6.02214076*10**23
ptables = fetch_table('elements')
density = ptables['density']
radius = ptables['atomic_radius']
mass = ptables['atomic_weight']
###


def gen_sys(weight = [1,2,2,2,1,4,1]):
    wt = np.sum(weight)
    r = random( )*wt
    k = 0
    for i in range(len(weight)-1):
        if r >= np.sum(weight[0:i+1]) and r < np.sum(weight[0:i+2]):
            k = i + 1
            break
#    print(k)
    return k
            
    

def gen_cell(V, sys):
    cell = np.ones(6) #a,b,c, alpha,beta,gamma
    r = V**(1/3)
    
    if sys == 0: #cubic
        cell[0:3] = cell[0:3] * r
        cell[3] = 90; cell[4] = 90; cell[5] = 90
        
    if sys == 1: #tentragonal
        cell[0:2] = uniform(0.5, 1.4)*r
        cell[2] = V/cell[0]/cell[1]
        cell[3] = 90; cell[4] = 90; cell[5] = 90
        
    if sys == 2: #orthorhombic
        cell[0] = uniform(0.5, 1.5)*r
        cell[1] = uniform(0.5, 1.5)*r
        cell[2] = V/cell[0]/cell[1]
        cell[3] = 90; cell[4] = 90; cell[5] = 90  
        
    if sys == 3: #hexagonal
        cell[0] = uniform(0.5, 1.4)*r
        cell[1] = uniform(0.5, 1.4)*r
        cell[2] = V/cell[0]/cell[1]/(np.sqrt(3)/2)
        cell[3] = 90; cell[4] = 90; cell[5] = 120
        
    if sys == 4: #trigonal

 #       print(cosa,cosb,cosr,(1-cosa**2-cosb**2-cosr**2) + 2*cosa*cosb*cosr)
        while True:
            cell[3:6] = uniform(60, 120)
            cosa = cos(cell[3]/180*pi)
            cosb = cos(cell[4]/180*pi)
            cosr = cos(cell[5]/180*pi)
            deno = (1-cosa**2-cosb**2-cosr**2 + 2*cosa*cosb*cosr)   
            if deno > 0:
                break              
        r3 = V/sqrt(deno)
        cell[0:3] = cell[0:3] * (r3)**(1/3) 
        
    if sys == 5: #monoclinic
        cell[0] = uniform(0.5, 1.5)*r
        cell[1] = uniform(0.5, 1.5)*r
        cell[5] = uniform(60, 120)
        cell[2] = V/cell[0]/cell[1]/sin(cell[5]/180*pi)
        cell[3] = 90; cell[4] = 90

    if sys == 6: #triclinic
        cell[0] = uniform(0.5, 1.5)*r
        cell[1] = uniform(0.5, 1.5)*r

        while True:
            cell[3] = uniform(60, 120)
            cell[4] = uniform(60, 120)        
            cell[5] = uniform(60, 120)
            cosa = cos(cell[3]/180*pi)
            cosb = cos(cell[4]/180*pi)
            cosr = cos(cell[5]/180*pi)
#        print((1-cosa**2-cosb**2-cosr**2) + 2*cosa*cosb*cosr)
            deno = (1-cosa**2-cosb**2-cosr**2) + 2*cosa*cosb*cosr
            if deno >0:
                break                             
        cell[2] = V/cell[0]/cell[1]/sqrt(deno)
    return cell

def gen_atom(n):
    pos = np.zeros((n, 3))
    for i in range(n):
        for j in range(3):
            pos[i, j] = random()
            
    return pos

def check(sys, rcut = 0.5 ):
    d = sys.get_all_distances(mic = True)
    #print('distance matrix', d)
    ind = sys.get_atomic_numbers()
    natom = len(ind)
    flag = True
    r = []
    for i in range(natom):
        r.append(radius[ind[i]-1]*0.01)
    # 0 is in distance matrix !!!!
    for i in range(natom):
        dis = np.delete(d[i, :], i)
        #print(dis)
        if np.min(dis) > 1.5*max(r):
            flag = False
            print('isolated atom', np.min(dis))
            break
        for j in range(i, natom):
            rA = radius[ind[i]-1]*0.01 #pm to angstrom
            rB = radius[ind[j]-1]*0.01 #pm to angstrom
            if i == j:
               continue 
            if d[i, j] < rcut*(rA + rB):
#                print(ind[i],ind[j],d[i, j], rcut*(rA + rB))
                flag = False
                print('small disance:', d[i, j], rA, rB)
                break
    return flag
            
def gen_V(ele, Natom, fix=False): #init Volume 50%-150% , fix==True, return fixed Volume
    
    V0 = []
    for i in range(len(ele)):
        #ind = 12-1
        ind = ptables[ptables.symbol==ele[i]]['atomic_number'].index
        rho = density.iloc[ind].iloc[0]
        m = mass.iloc[ind].iloc[0]
        r = radius.iloc[ind].iloc[0]*0.01 #pm to angstrom
        if rho > 0.1:   # for solid element
            V0.append(10**24/NA*m/rho) #(g/NA)/(g/cm3) = 10^24*A^3/NA
        else:  # for gas element
            V0.append(4/3*r**(3))
    V = np.sum(V0)
    if fix:
        return V
    Vi = V*uniform(0.8, 4.0)
    return Vi

def gen_one(ele, Natom, filename, weight, rcut, form):
    comp = ''
    for i in range(len(ele)):
        comp = comp + ele[i] + str(Natom[i])
    #print(comp)
    while True:
        crystal = gen_sys(weight)
        Vi = gen_V(ele, Natom)
        cell = gen_cell(Vi, crystal)
        pos = gen_atom(np.sum(Natom))
        #print(rcut, comp, pos, cell)
        sys = Atoms(comp, scaled_positions = pos, cell = cell, pbc=[1, 1, 1])    
        flag = check(sys, rcut)
        #print(flag)
        if flag == True:
            break
    if form == 'extxyz':
       extxyz.write_extxyz(filename, sys) 
    else:
        write(filename, sys, format=form)
    return sys

def gen(inp, ele, Natom_list, nsys, name, system_weight, spg, Natom_weight=[], cellbounds=None, rcut=0.5, form='vasp'):
    if os.path.exists(inp):
        print('input files already exist')
     #   os._exit(0)
    else:
        os.system('mkdir ' + inp )
    syss = []
    if len(Natom_weight)==0:
        Natom_weight = np.ones(len(Natom_list))
    Natom_dist = choices(Natom_list, weights = Natom_weight, k = nsys-len(Natom_list))
    Natom_dist = Natom_list + Natom_dist
    print(Natom_dist)
    f1 = open('gen_info.dat', 'w')
    print(cellbounds)
    for i in range(nsys):
        filename = inp + '/' + name + '_' + str(i) + '.' + form
       
        if len(cellbounds)==0 and spg == None:
            sys = gen_one(ele, Natom_dist[i], filename, system_weight, rcut, form)
        elif len(cellbounds)>0 and spg == None:
            volume = gen_V(ele, Natom_dist[i])
            Lmax = 3*(volume)**(1/3)
            cellbounds['a'][1] = Lmax; cellbounds['b'][1] = Lmax; cellbounds['c'][1] = Lmax;
            #print(cellbounds)
            sys = gen_ase(ele, Natom_dist[i], volume, cellbounds, filename, N=1, rcut=rcut, form=form)
        else:
            #print('Using randSpg')
            volume = gen_V(ele, Natom_dist[i])
            for gen_max in range(10):
                rand = uniform(1.0, 5.0)
                Lmax = rand*(volume)**(1/3)
                volume = rand*volume
                cellbounds['a'][1] = Lmax; cellbounds['b'][1] = Lmax; cellbounds['c'][1] = Lmax;
                if spg == 0:
                    spacegroups = str(randint(1, 230))
                else:
                    spacegroups = str(sample(spg,1) )
                composition = ''
                for ie in range(len(ele)):
                    composition = composition + ele[ie] + str(Natom_dist[i][ie])
                #print(composition)
                sys = randSpg(composition=composition, outname=filename, maxVolume=volume, spg=spacegroups, 
                        cellbounds=cellbounds, rmin=rcut, outputDir='temp')
                if sys != False:
                #print(sys)
                    break
        if sys == False:
            continue
        syss.append(sys)
        cell =  sys.cell.cellpar()
        f1.write( format(i, '<6d') + ' ')
        f1.write(sys.get_chemical_formula() + ' ')
        for j in range(len(cell)):
            f1.write( format( (cell[j]), '>7.2f') + ' ')
        f1.write('\n')
    f1.close()
    return syss

def gen_ase(ele, Natom, volume=None, cellbounds=None, filename=None, N=1, rcut=0.5, form='vasp'):
    #volume: Target cell volume for the initial structures, in angstrom^3
    # Specify the 'building blocks' from which the initial structures
    if volume == None:
        volume = gen_V(ele, Natom, fix=True)
        Lmax = 3*(volume)**(1/3)
    if cellbounds == None:
        cellbounds ={'phi': [20, 160], 'chi': [20, 160],
            'psi': [20, 160], 'a': [2, Lmax],
            'b': [2, Lmax], 'c': [2, Lmax] }
        
    blocks = []
    Z = []
    #stoichiometry = []
    for i in range(len(ele)):
        blocks = blocks + [ele[i]] * Natom[i]
        #Z.append(atomic_numbers[ele[i]])
    for i in range(len(blocks)):
        Z.append(atomic_numbers[blocks[i]])
    # Generate a dictionary with the closest allowed interatomic distances
    blmin = closest_distances_generator(atom_numbers=Z,
                                    ratio_of_covalent_radii=rcut)

    # Specify reasonable bounds on the minimal and maximal
    # cell vector lengths (in angstrom) and angles (in degrees)
    cellbounds = CellBounds(bounds=cellbounds)

    # Choose an (optional) 'cell splitting' scheme which basically
    # controls the level of translational symmetry (within the unit
    # cell) of the randomly generated structures. Here a 1:1 ratio
    # of splitting factors 2 and 1 is used:
    splits = {(2,): 1, (1,): 1}
# There will hence be a 50% probability that a candidate
# is constructed by repeating an randomly generated 
# structure along a randomly chosen axis. In the other 50%
# of cases, no cell cell splitting will be applied.

    slab = Atoms('', pbc=True)
    
# Initialize the random structure generator
    sg = StartGenerator(slab, blocks, blmin, box_volume=volume,
                    number_of_variable_cell_vectors=3,
                    cellbounds=cellbounds, splits=splits)
    syss = []
    for i in range(N):
        sys = sg.get_new_candidate()
        syss.append(sys)
        if filename != None:
            if form == 'extxyz':
                extxyz.write_extxyz(filename, sys)
            else:
                write(filename, sys, format=form)
    if N == 1:
        return sys
    else:
        return syss

