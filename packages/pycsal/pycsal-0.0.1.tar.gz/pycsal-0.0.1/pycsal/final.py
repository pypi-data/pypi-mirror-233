from opt import *
from gen_stru import gen
from pick import pick
from interface_deepmd import *
from deepmd.calculator import DP
from tool import *
cmds = ["pair_style meam",
        "pair_coeff * * library.meam Mg Sn  MgSn.meam Mg Sn"]
lammps = LAMMPSlib(lmpcmds=cmds, logfile='test.log', keep_alive = True )
calculator = lammps  ## target potential, MEAM/DFT
train_path = 'train'
#fitter = DP(model= train_path + "/graph.pb")
ele = ['Mg', 'Sn']
Natom = [4, 2]
nsys = 50
nstep = 20 
keep_ratio = 0.9
Ecut = -0.2
#### default parameters less modified
weight = [1,0,0,1,0,0,0] ##weight for 7 crystal systems
min_data = 10    ###minimal amount of new data for refitting a ML potential
Econv = 0.005  ### fitter RMES < EconV eV , stop
max_keep = 1000
####--------------------------
count = 0
name = ''
for i in range(len(ele)):
    name = name + ele[i] + str(Natom[i])
name = name + '_'


def finalize(ele, Natom, step, nsys, name, weight, calculator, E0, EHull=-0.0):
    inp = 'init' + str(step)
    out = 'out' + str(step)
    fin = 'final'
    fitter = DP(model= train_path + "/graph.pb")

#    gen(inp, ele, Natom, nsys, name, weight)
#print("start optimziation step %d" %(step))
#    opt(inp, out, step, nsys, name, calculator, fitter, train_path='train')
    fitter = calculator
    MLP_out = np.loadtxt(out + '_info.dat')
    Ef=0
    for i in range(len(Natom)):
        Ef = Ef + E0[i]*Natom[i]
    MLP_E = (MLP_out[:, 1] - Ef )/np.sum(Natom)
    os.system('mkdir ' + fin + '_init')
    for i in range(len(MLP_E)):
        if MLP_E[i] < EHull:
            os.system('cp ' + out + '/' + name + str(i) + '_out.vasp ' + fin + '_init')
            print(MLP_E[i],'cp ' + out + '/' + name + str(i) + '_out.vasp ' + fin + '_init')

    
    #opt(out, fin, step, nsys, name, calculator, fitter, train_path='train')
E0 = [-1.549343, -3.1399035 ]
nsys=1000
finalize(ele, Natom, nstep, nsys, name, weight, calculator, E0)    
