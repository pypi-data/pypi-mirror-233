import unittest
from pyxtal import pyxtal
from random import randint
from ase.ga.utilities import CellBounds
import numpy as np

class Test_pyxtal(unittest.TestCase):
    def test_random_crystal(self):
        my_crystal = pyxtal()
        my_crystal.from_random(3, 99, ['Ba','Ti','O'], [1,1,3])
        #my_crystal
    def test_ase_format(self):
        def check(sys, rcut = 0.5 ):

            d = sys.get_all_distances(mic = True)
            #print('distance matrix', d)
            ind = sys.get_atomic_numbers()
            natom = len(ind)
            radius = [100]*natom
            flag = True
            r = []
            for i in range(natom):
                r.append(radius[i]*0.01)
            # 0 is in distance matrix !!!!
            for i in range(natom):
                dis = np.delete(d[i, :], i)
                #print(dis)
                if np.min(dis) > 1.5*max(r):
                    flag = False
                    print('isolated atom', np.min(dis))
                    break
                for j in range(i, natom):
                    rA = radius[i]*0.01 #pm to angstrom
                    rB = radius[j]*0.01 #pm to angstrom
                    if i == j:
                        continue 
                    if d[i, j] < rcut*(rA + rB):
        #                print(ind[i],ind[j],d[i, j], rcut*(rA + rB))
                        flag = False
                        print('small disance:', d[i, j], rA, rB)
                        break
            return flag
        
        cellbounds = {'phi': [20, 160], 'chi': [20, 160], 'psi': [20, 160], 'a': [2, 5], 'b': [2, 5], 'c': [2, 5] }
        cellbounds = CellBounds(bounds=cellbounds)
        my_crystal = pyxtal()
        while True:
            spg = randint(1, 230)
            #spg = 55-56
            try:
                my_crystal.from_random(3, spg, ['P'], [12])
            except:
                continue
            sys = my_crystal.to_ase()
            flag = check(sys, rcut=0.5)
            if flag == False:
                continue
            cell = sys.get_cell()
            if cellbounds.is_within_bounds(cell):
                break
            else:
                print(cell)

        sys.write('1.xyz', format='extxyz')
        print(sys.cell.cellpar())
        cell[0:3] = cell[0:3]*np.random.uniform(0.95, 1.05, 3) #random displacement on length
        cell[3:6] = cell[3:6] + np.random.uniform(-3, 3, 3) #random displacement on angles
        sys.set_cell(cell) 
        sys.rattle(stdev=0.01) #random displacement on atomic coordinate with a normal distribution
        return sys
unittest.main()