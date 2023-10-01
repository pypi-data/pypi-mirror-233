# A Python package for crystal search with active learning (pycsal) :smile:
# Documention (in prepare)  :joy:
# Brief introduction  
It is designed for searching alloys with active learning. Fitting a machine learning potential (MLP) can reduce the computational costs with only using ab inito calculations to find stable crystals of alloys. Currently, the workflow is divided into two parts, as shown in Fig. 1a. The first part is to generate a MLP potential with random and search active learing. The second part is to search crystal with genetical algorithm and the generated MLP portential. For a single system with one atomic combination, the genetic algorithm can be used to generate new structures to up data the MLP instead of randomly generated strutures in Fig. 1b.

![Fig. 1 Illustration of the program.](figures/search_ga.jpg)

**Fig. 1 Illustration of the program.**

## Supported packages for calculating and fitting potentials
VASP is supproted for DFT calculations in searching crystals. In addition, the LAMMPSlib interface with semi-empircal potential to replace DFT for debugging program. Two machine learning potential packages are supported to train the DFT calculations, “[deepmd-kit](https://github.com/deepmodeling/deepmd-kit)” and “[reann](https://github.com/zhangylch/REANN)”. Look the official documents and install them by yourself! 
## Input files
The input file for setting active learning and genetic algorithm should be provide in "yaml" format. Set input parameters in “search.yaml” as the following previous instructions. The calculation parameters of VASP is provided in "vasp.yaml".

# Tips
 1. Using different Python when using different MLP packages. As reann needs to install torch, deepmd-kit cannot run due to the conflicts of Python packages.
 2. Make sure your "input.json" is correct for using deepmd-kit. In particular, there parameters should be carefully checked: "sel", "systems".

# Installation & requirements
These python packages are required for using this code: [mendeleev](https://mendeleev.readthedocs.io/en/stable/), [ase](https://wiki.fysik.dtu.dk/ase/), [asaplib](https://github.com/BingqingCheng/ASAP). Environment variables of ASE interfaces should be set for using ASE to call LAMMPS and VASP. You can read the document on ASE calculators.
 There are examples of using the program.
## Installation of required python packages
```bash
pip install ase mendeleev asaplib pyxtal
pip install git+https://github.com/ulissigroup/vasp-interactive.git
```
## Installation of randspg for spage group specified initiation (optional)
```bash 
git clone https://github.com/psavery/randSpg  
cd randSpg  
mkdir build  
cd build  
cmake ..  
make 
```
## Installation of deepmd-kit
Please read its official document for [installation](https://github.com/deepmodeling/deepmd-kit/blob/master/doc/install/easy-install.md#install-off-line-packages). There is an example of off-line installation:
```bash
wget https://github.com/deepmodeling/deepmd-kit/releases/download/v2.2.3/deepmd-kit-2.2.3-cuda11.6_gpu-Linux-x86_64.sh.0
wget https://github.com/deepmodeling/deepmd-kit/releases/download/v2.2.3/deepmd-kit-2.2.3-cuda11.6_gpu-Linux-x86_64.sh.1
cat deepmd-kit-2.2.3-cuda11.6_gpu-Linux-x86_64.sh.0 deepmd-kit-2.2.3-cuda11.6_gpu-Linux-x86_64.sh.1 > deepmd-kit-2.2.3-cuda11.6_gpu-Linux-x86_64.sh
bash deepmd-kit-2.2.3-cuda11.6_gpu-Linux-x86_64.sh
```
## Patching VASP source codes to accelerate calculations with ASE interface.
Optimization with original ASE-VASP interface is many times slower than using VASP directly. We use the [vasp-interactive](https://github.com/ulissigroup/vasp-interactive) patch with comparable speed than pure VASP. In order to optimize the cell, the source code of VASP should be patched following the instruction of [vasp-interactive](https://github.com/ulissigroup/vasp-interactive). <font color=red> In a word, you need to re-compile you VASP!! Then, install the python interface of vaps-interactive. </font> If you want to use the orginal ASE-VASP interface, see the parameter 'ASE-VASP' in vasp.yaml.
## Setting ASE environment variable.
The [LAMMPS interface](https://wiki.fysik.dtu.dk/ase/ase/calculators/lammps.html) and [VASP psedopotential](https://wiki.fysik.dtu.dk/ase/ase/calculators/vasp.html) should be set for using ASE.
```
export ASE_LAMMPSRUN_COMMAND=" xxx/lmp"
export VASP_PP_PATH=xxxx/potentials
```
## How to use this code
### Download this code
```bash
git clone https://github.com/phys-chem/search
```
### Use this code
#### generating a MLP potential
prepare input files and "python main.py":
```bash
python xxxx/search/main.py
```
#### searching with the genetic algorithm (GA) implemented in ASE
Please revise the code of "ga.py", set the file of MLP potential and GA parameters. This part is still under revision for better use!
```
python ga.py
```
# Examples
## Lennard-Jones crystals
The Lennad-Jones calculator of ASE is used for calculating LJ crystals. The "examples/LJ/" directory includes a yaml file for searching parameters and json files for deepmd-kit training.  
`examples/LJ/search.yaml`    
`examples/LJ/train/input0.json`  
`examples/LJ/train/input1.json`  

# **Parameters of input files**
## Parameters of search.yaml for active learning:
**init**: *int, default:4*
init=1, generation of a cell by randomizing crystal systems.  
init=2, random generation using ase.ga.startgenerator. In addition, an isolated atom, with no interatomic distance smaller than double the sum of atoms’ radii, is not counted. The criterion for a reasonable configuration is stricter than init=1.  
init=3, generation with space group constraint by [randSpg](https://github.com/psavery/randSpg) package.  
init=4, generation with space group constraint by [Pyxtal](https://pyxtal.readthedocs.io/en/latest/) package.  

**ele**: *list*  
A list contains all elements of the system, like [‘Mg’, ‘Sn’] for Mg-Sn alloy.

**Natom_list**: *list*  
A list contains the number of atoms for each subsystem. Each object in “Natom_list” is also a list. [[4, 2], [4, 1]] denotes two subsystems Mg4Sn2 and Mg4Sn for “ele” equaling [‘Mg’, ‘Sn’]. 
 
**calculation**: *str*  
the calculator of the potential we want to fit. Set it as “lammps” and provide
the “cmds” parameters for initializing the ASE-LAMMPS interface: ase.calculators.vasp.LAMMPSlib(lmpcmds=cmds)
Set it as “vasp” and provide the “vasp.yaml” for initializing the VASP interface, the default is "vasp_interactive.VaspInteractive". See the parameter "VASP_ASE". Set it as "LJ" by using the ase.calculators.lj for using Lennard-Jones potential.

**VASP_ASE**: *bool*, default: False  
If it is False, interactive VASP interface "vasp_interactive.VaspInteractive" is used. If it is True, the default ASE-VASP interface "ase.calculators.vasp.Vasp()" is used without installing the "vasp-interactive" package.

**E0**: *list, default: np.zeros(len(ele))*    
A list contains the formation energy per atom for each element. The length should equal the “ele”, it can be calculated by calculating a crystal of each element. 

**ninit**: *int, default: 20*   
The initial number of generated structures for further relaxation constructs an initial dataset for fitting.

**niter**: *int,  default: 40*   
The number of generated structures for relaxation with MLP is set. Their final configurations will be selected.  

**Ecut**: *float*, default: 1.0  
  Configuration with energy lower than the formation energy than “Ecut” will be chosen to calculate the error separately. 

**rcut**: *float*, default: 0.7   
  The minima interatomic distance is calculated by “rcut” multiplying the sum of two atoms’ radii. 
The structure is not counted if a pair of atoms is closer than the distance. A new structure will be generated to meet the criterion. Its value should be too significant, especially for a large system. Otherwise, the program can get struck in generation instead of running. 

**Natom_weight**: *list, default: []*    
Its length is same as “Natom_list”—the weight of each subsystem for generating random configuration in search processing.

**system_weight**: *list, default: [1,1,1,1,0,0,0]*  
The generation code is made by ourselves. Its length is same as “Natom_list”. If it is provided, configurations are randomly generated in 7 types of crystal with the weight. The weight is set for cubic, tetragonal, orthorhombic, hexagonal, trigonal, monoclinic, and triclinic systems, respectively.

**cellbounds**: *dict, default: cellbounds = {'phi': [30, 150], 'chi': [30, 150], 'psi': [30, 150], 'a': [2, 5], 'b': [2, 5], 'c': [2, 5] }*   
Example: {'phi': [20, 160], 'chi': [20, 160], 'psi': [20, 160], 'a': [2, 5], 'b': [2, 5], 'c': [2, 5] }. The parameter denotes the range of six crystal parameters for a randomconfiguration. 

**spg**: *int or str, default:0*
Structures will be generated with assigned spacegroups by combining Wyckoff positions using the [randSpg](https://github.com/psavery/randSpg) or [Pyxtal](https://pyxtal.readthedocs.io/en/latest/) package. Random spacegroup will be assigned when “spg” is 0. Otherwise, spacegroups are set as a string following the format of the parameter “spacegroups” of randSpg. Then, small displacement will be added in these structures. 

**Econv**: *float (eV/atom), default: 0.005*  
If the energy RMSE of MLP potential is lower than “Econv”, the program will stop.

**nstep**: *int, non-negative, default: 20*  
The maximum iteration step.

**sstep**: *int, non-negative, default: 0*   
It is the starting iteration step for a restarting calculation.

**start_opt**: *int, default: 0*  
It is a index for restaring calculations. For example, program stops optimization of a structure, you can start with the structure with the index.

**potential**: *“deepmd” or “reann”*  
It is the MLP model used for fitting our calculator. You can choose one of them; their input files should be prepared after installing these packages. 
When using “[deepmd](https://github.com/deepmodeling/deepmd-kit)”, you need to make a file folder named the value of “train_path” in the current path. 
Prepare two “input.json” for using DeepMD: “input0.json” for the first training and “input1.json” for further training. The “input1.json” reads the parameters of previous training. 
The “../training_data/chemical_formula” should be written in the JSON file, similar to the validation data. When using “[reann](https://github.com/zhangylch/REANN)”, 
you need to make a file folder named the value of “train_path” in the current path. Similarily, you need to prepare “input0_nn” and “input1_nn” for the “input_nn” file of “REANN”. In addition, you should also provide “input_denisty”.  

**reann_exe**: str  
It is the command runing "reann" source code when using reann potential for fitting, for example: 'python3.9 -m torch.distributed.run --nproc_per_node=1 --nnodes=1 --standalone xxxx/REANN-main/reann'. Specify your Python and reann directory. 

**keep_ratio**: *float between 0 and 1, default: 0.5*    
The percentage during the selection process, only a part of the data generated by MLP is verified by a calculator (DFT) to enlarge the data and re-fit MLP. The PCM analysis with the SOAP descriptor using the “asaplib” package is used for selection.

## Parameters of search.yaml for genetic algorithm:

**switch_ga**: *int*, default: 1e7    
The number of step switch from random search to genetic algorithm. It is only available for a single system.

**database**: *str*, default: 'gadb.db'
The name of ASE database for running genetic algorithm.

**population_size**: *int*, default: 20
As the name indicates, it is the population size running genetic algorithm.  
 !-----------------------------------------------------------------------

## Parameters of vasp.yaml:
When the parameter "calculation" is "vasp", the parameters of vasp calculation should be provided in "vasp.yaml "as the "yaml" format:  
**ASE-VASP**: *bool, default: False*
Whether the orginal ASE-VASP interface should be used. Please set the parameters as True if you don't re-compile you VASP with interactive patch.

**nprocess**: *int, default: 1*  
The available number of cores for performing VASP calculations.  

**command** : *str, default:'vasp_std'*  
The command for running vasp, set the environmental variables or the absoulte path.

**xc** : *str, default:'PBE'*
The name of a density functional in VASP.

**encut** : *int*  
Plane wave cut-off energy, the ENCUT parameter in VASP.

**ispin** : *int, default: 1*   
Flag for spin-polarization calculation, the ISPIN parameter in VASP.

**kpts** : *list with three int elements, default: [1,1,1]*  
K-points mesh for VASP.

**sigma**: *float, default: 0.05*  
The SIGMA parameter in VASP.

**isym** : *int, default: 0*  
The ISYM parameter in VASP.

**npar**: *int, default will automatically calculated*  
The NPAR parameter in VASP.

**algo**: *str, default: 'fast'*  
The ALGO parameter in VASP.


## Parameters for debugging:
**rLJ**: *float*, default: 6.0*  
It is the cutoff radii of Lennard-Jones potenitial. It works only when "calculation" is "LJ".  
