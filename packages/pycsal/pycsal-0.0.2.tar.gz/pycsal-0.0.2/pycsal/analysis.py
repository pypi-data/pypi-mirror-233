#from ase import Atom, Atoms
import numpy as np
import os
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.vasp import Poscar
from pymatgen.core import Structure, Lattice
#from gen_stru import ge
def refine(inp, out, name, nfile, form='vasp'):
    V_tol = 1.0*0.01 #volume difference lower than V_tol% regarded as same
    form = 'vasp'
    #nfile = 100
    #inp = 'out'
    #out = 'refine'
    sym_out = 'sym'
    if not os.path.exists(inp):
        print('input files not exist')
        os._exit()
    if not os.path.exists(out):
        os.system('mkdir ' + out )
    else:
        os.system('rm -r' + out)
    if not os.path.exists(sym_out):
        os.system('mkdir ' + sym_out )
    else:
        os.system('rm ' + sym_out + '/*')

    cry = []
    mols = []
    f1 = open(str(name) + '' + str(nfile) + '_analysis.dat', 'w')

    if format == 'vasp':
        for i in range(0, nfile):
    #sys = read( filename= path + name + str(i) + '_out.vasp',format='vasp')
    #mol = AseAtomsAdaptor().get_structure(sys)
#    print('analysis: ' + str(i))
            fin = inp + '/' + name + str(i) + '_out.' + form
            if os.path.exists(fin) == False:
                print('file not exist: ', i, fin)
                continue
            mol = Structure.from_file(inp + '/' + name + str(i) + '_out.' + form)
            mols.append(mol)
    #if format == 'vasp'

    for i in range(len(mols)):
        mol = mols[i]
        SA = SpacegroupAnalyzer(mol, symprec=0.05, angle_tolerance=5.0)
#    print(SA._space_group_data)
        if SA._space_group_data is None:
            print(str(i) + ' is None')
            continue
        SGN = SA.get_space_group_number()
        SGS = SA.get_space_group_symbol()
        struct = SA.get_refined_structure()

        cell = list(struct.lattice.abc) + list( struct.lattice.angles)
        vol = struct.volume
        natom = len(struct.atomic_numbers)
#    print(struct.atomic_numbers)
        poscar = Poscar(struct)
        poscar.write_file(filename= out + '/' + name + str(i) + '_refine.'+form, significant_figures=16)
        f1.write( format(i, '<6d') + ' ')
        f1.write( format(SGN, '<4d') + ' ')
        f1.write( format(SGS, '<10s') + ' ')

        f1.write(format(natom, '<4d') + ' ')
        f1.write(format(vol, '<10.3f') + ' ')
        for j in range(6):
            f1.write(format(cell[j], '<7.2f') + ' ')
        f1.write('\n')
        cry.append([SGN, vol, natom, cell, i ])
    f1.close()


    new = [cry[0]]; freq =[0]
    write_sym(cry[0], 0, sym_out)
    
    for i in range(len(cry)):
        for j in range(len(new)):
            if is_same_cell(cry[i], new[j], V_tol): #same structure
                freq[j] = freq[j] + 1
                break #exit the loop
            if j == len(new)-1:
                freq.append(1) # not finded in new[]
                new.append(cry[i])
                write_sym(cry[i], cry[i][4], sym_out)

# open file in write ode
    with open(str(name) + '' + str(nfile) + '_crystal.dat', 'w') as fp:
        fp.write('#spacegroup volume natom freq\n')
        for i in range(len(new)):
            # write each item on a new line
            #print("%4d %10.2f %4d \n", %(new[i][0], new[i][1], freq[i])  )
            fp.write(format(new[i][0], '<4d') + ' ' + format(new[i][1], '8.2f') + 
                ' ' + format(new[i][2], '<4d') + ' ' + str(freq[i]) + '\n'  )
    print('Done')
######

###remove structures with large volume:
    files = os.listdir(sym_out)
    V0 = np.zeros( len(files) )

    for i in range(len(files)):
        temp = files[i].replace('.'+form, '')
        temp = temp.split('_')
        V0[i] = float(temp[2])/float(temp[3])
#    print(temp[2],temp[3], V0[i])
    Vmin = min(V0)
    Vper = V0/Vmin - 1
    for i in range(len(files)):
        if Vper[i] > 30*0.01:
            print(Vper[i],' rm ' + sym_out + '/' + files[i] )
            os.system('rm ' + sym_out + '/' + files[i] )
###
def write_sym(cry, ind, sym_out, cut=2, form='vasp' ):
    if cry[0] > cut:
        sym = sym_out + '/' + name + str(cry[0]) + '_' + format(cry[1], '.2f') \
                + '_' + str(cry[2])+ '.' + form
        os.system('cp ' + out + '/' + name + str(ind) + '_refine.' + form + ' ' + sym)
    
def is_same_cell(c1, c2, V_tol):
    flag = True
    if c1[0] != c2[0]:
        return False
    if abs(1-c1[1]/c2[1]) > V_tol:
        return False
    abc = [1, 1]; a3 = [0, 0] 
    for i in range(3):   #c1,c2[3] is the cell length and angles
        abc[0] = abc[0]*c1[3][i]
        abc[1] = abc[1]*c2[3][i]
        a3[0] = a3[0] + c1[3][i]**3
        a3[1] = a3[1] + c2[3][i]**3

#permutation invarient polymomials(PIPs): Volume, abc, a^3+b^3+c^3
#compared PIP to exclude same cells
    if abs(1-c1[1]/c2[1]) > V_tol:
        return False
    if abs(1-abc[0]/abc[1]) > V_tol: 
        return False
    if abs(1-a3[0]/a3[1]) > V_tol:
        return False
    return True

inp = 'final'
out = 'refine'
nfile = 1000
name = 'Mg4Sn2_'
refine(inp, out, name, nfile, form='vasp')
