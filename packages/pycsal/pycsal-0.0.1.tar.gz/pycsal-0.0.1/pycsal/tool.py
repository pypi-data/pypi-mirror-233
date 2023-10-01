import os
import numpy as np

#def read_input(input = 'search.yaml')
    

def asap_select(inp, out, nstep, nkeep):

    if os.path.exists(inp + '.xyz'):
        os.system('rm ' + inp + '.xyz')
    for i in range(1, nstep+1):
        os.system('cat ' + inp + str(i) + '.xyz >> ' + inp + '.xyz')
    os.system('asap gen_desc -f ' + inp + '.xyz soap > soap.log 2>&1 ' )
    print('asap gen_desc -f ' + inp + '.xyz soap > soap.log' )

    os.system("asap select -f ASAP-desc.xyz -dm '[*]' -n " + str(nkeep)
            + ' -p ' + out  + ' --savexyz > soap.log  2>&1')

    print("asap select -f ASAP-desc.xyz -dm '[*]' -n " + str(nkeep)
            + ' -p ' + out  + ' --savexyz ')

def get_xyz_frames(fname): 
    if not os.path.exists(fname):
        return 0

    f1 = open(fname, 'r')
    ip = 0
    while True:
        line = f1.readline()
        if not line:
            break
        ip = ip + 1
        natom = int(line.split()[0])
        for i in range(natom + 1):
            f1.readline()
    f1.close()
    return ip

def delete_xyz_frames(infile, outfile, delete_id):
    if not os.path.exists(infile):
        return 0
    ip = -1    
    f1 = open(infile, 'r')
    f2 = open(outfile, 'w')
    while True:
        line = f1.readline()
        if not line:
            break
        ip = ip + 1
#        print(line + '11')
        temp = line.split()
        natom = int(temp[0])
#        print(natom, 'test')
#        lines = f1.readlines(natom+1)
        if delete_id[ip]:
            f2.write(line)
            for i in range(natom+1):
                line = f1.readline()
                f2.write(line)
        else:
            for i in range(natom+1):
                f1.readline()

    f1.close()
    f2.close()
    
def split_xyz(fname, outname):
    f1 = open(fname, 'r')
    formulars = []
    count = -1
    while True:
        line = f1.readline()
        if not line:
            break
        count = count + 1
        line_list = [line]
        natom = int(line.split()[0])
        line_list.append(f1.readline())
        comp = []
        for i in range(natom):
            line = f1.readline()
            line_list.append(line)
            comp.append(line.split()[0])

        ele = sorted(set(comp), key=comp.index)

        formular = '' 
        for item in ele:
            count = comp.count(item)
            if count == 1:
                formular = formular + item
            else:
                formular = formular + item + str(count)
        
        if formular not in formulars:
            formulars.append(formular)
            os.system('rm ' + formular+ '_' + outname + '.xyz')
        with open(formular+ '_' + outname + '.xyz' , 'a') as fout:
            for line in line_list:
                fout.write(line)
    f1.close()
