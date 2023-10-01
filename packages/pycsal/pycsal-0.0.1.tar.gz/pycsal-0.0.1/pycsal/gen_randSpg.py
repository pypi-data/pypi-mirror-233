from ase.data import atomic_numbers, covalent_radii
from ase.io import read
import os
import re
import numpy as np
import random
import math
def randSpg(composition, spg, cellbounds, outname, fname='randSpg.in', minVolume=-1, maxVolume=-1, ngen=1, general='false', rmin=0.5, outputDir='randSpg', adj_mat=[]):
# Composition is set by atomic symbols followed by number as such:
    ele = re.sub('[0-9]', ' ', composition)
    ele = ele.split() #get the element symbol from chemical formula
    radii = []
    for i in range(len(ele)):
        radii.append( covalent_radii[ atomic_numbers[ele[i]] ] ) #get atomic radii     
    if len(adj_mat) == 0:
        adj_mat = np.ones( (len(ele), len(ele)) )
    with open(fname, 'w') as f: # write the input file of randSpg
        f.write('comment line \n')
        f.write('composition = ' + composition + '\n')
        f.write('spacegroups = ' + spg + '\n')
        f.write('latticeMins = ')
        f.write(str(cellbounds['a'][0]) + ', ' + str(cellbounds['b'][0]) + ', ' + str(cellbounds['c'][0]) + ', ' ) 
        f.write(str(cellbounds['phi'][0]) + ', ' + str(cellbounds['chi'][0]) + ', ' + str(cellbounds['psi'][0]) + '\n')
        f.write('latticeMaxes = ')
        f.write(str(cellbounds['a'][1]) + ', ' + str(cellbounds['b'][1]) + ', ' + str(cellbounds['c'][1]) + ', ' )
        f.write(str(cellbounds['phi'][1]) + ', ' +str( cellbounds['chi'][1]) + ', ' + str(cellbounds['psi'][1]) + '\n')
        f.write('minVolume = ' + str(minVolume) + '\n')
        f.write('maxVolume = ' + str(maxVolume) + '\n')
        f.write('numOfEachSpgToGenerate = ' + str(ngen) + '\n')
        f.write('forceMostGeneralWyckPos = ' + general  + '\n')
        for i in range(len(ele)):
            for j in range(i, len(ele)):
                if adj_mat[i, j] == 1:# min(distance)>rcut*(rA+rB)
                    f.write('customMinIAD ' + ele[i] + ' ' + ele[j] + ' = ' + str(rmin*(radii[i]+radii[j])) + '\n')
                elif adj_mat[i, j] != 1: #min(distance)>adj_mat[i, j]*(rA+rB)
                    f.write('customMinIAD ' + ele[i] + ' ' + ele[j] + ' = ' + str(adj_mat[i, j]*(radii[i]+radii[j]))+ '\n') 
                #else:
                #    f.write('customMinIAD ' + ele[i] + ' ' + ele[j] + ' = ' + str(1*(radii[i]+radii[j])) + '\n')             
        #f.write('setMinRadii = ' + str(rmin) + '\n')
        f.write('outputDir = ' + outputDir  + '\n')
    if os.path.exists(outputDir):
        os.system('rm -r ' + outputDir)
    os.system('randSpg ' + fname)
    syss = os.listdir(outputDir)
    if len(syss) == 0:
        return False
    for sys in syss:
        os.system('mv ' + outputDir + '/' + sys + ' ' + outname )
        sys = read(outname, format='vasp')
        cell = sys.cell.cellpar()
        for i in range(6):
            if math.isnan(float(cell[i])) == True: #Sometimes, the randSpg writes a POSCAR with cell parameters as "nan".
                return False
        cell[0:3] = cell[0:3]*np.random.uniform(0.95, 1.05, 3) #random displacement on length
        cell[3:6] = cell[3:6] + np.random.uniform(-3, 3, 3) #random displacement on angles
        sys.set_cell(cell) 
        sys.rattle(stdev=0.01) #random displacement on atomic coordinate with a normal distribution

    return sys


