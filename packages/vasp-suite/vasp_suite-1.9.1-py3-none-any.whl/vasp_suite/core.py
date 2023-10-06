'''
A programme which holds the core functions of vasp_suite.
'''

# Imports
import numpy as np
import os

from .structure import Structure, Dope, Molecule
from .input import InputFileGenerator
from .submission import SubmissionWriter
# Functions


def generate_input(filename: str, calculation: str):
    '''
    Generates Input files for VASP Calculations.

    Parameters
    ----------
    filename : str
        The name of the input file to be generated.
    calculation : str
        The type of calculation to be performed.
    '''
    input_files = InputFileGenerator(filename, calculation)
    input_files.generate_incar()
    input_files.generate_potcar()


def generate_job(title, cores, vasp_type, conv):
    '''
    Generates a submission script for VASP calculations.

    Parameters
    ----------
    title : str
        The title of the job.
    cores : int
        The number of cores to be used.
    vasp_type : str
        The type of VASP calculation to be performed. vasp_std or vasp_gam.
    '''
    job = SubmissionWriter(title, cores, vasp_type, conv)
    if job.hostname == 'csf3':
        job.submission_csf3()
    elif job.hostname == 'csf4':
        job.submission_csf4()
    else:
        exit()


def generate_supercell(expansion: np.ndarray, filename: str):
    '''
    Generates a supercell from a given expansion matrix.

    Parameters
    ----------
    expansion : np.ndarray
        The expansion of each lattice vector.
    filename : str
        The name of the file to be expanded.
    '''
    struct = Structure.from_poscar(filename)
    struct.generate_supercell(n=expansion)
    struct.reorder_supercell()
    struct.write_poscar('POSCAR_supercell')


def dope_structure_sym(filename: str, dopant: str, replace: str, instances: int, no_sym: bool):
    struct = Dope(filename, dopant, replace, instances)
    print('Spacegroup: {}'.format(struct.spacegroup))
    struct.generate_structures()
    if not no_sym:
        struct.symmetrize()
    struct.write_poscars()


def generate_defect(filename: str, site: str, instances: int):
    '''
    Generates a defect structure from a given structure.

    Parameters
    ----------
    filename : str
        The name of the file.
    site : str
        The site to be removed.
    instances : int
        The number of instances of the defect.
    '''
    _d = Dope(filename, 'D', site, instances)
    _d.generate_structure()
    _d.Create_defect()
    _d.write_poscars()


def calculate_kpoints(filename: str) -> None:
    '''
    Calculates possible kpoint meshes for a given structure.
    
    Parameters
    ----------
    filename : str
        The name of the file to be analysed.
    '''
    struct = Structure.from_poscar(filename)
    mesh, density = struct.calculate_mesh()
    for i in range(len(mesh)):
        print(f'Mesh: {mesh[i][0]} {mesh[i][1]} {mesh[i][2]} Density: {density[i]}')
    return None

def generate_kpoints(mesh: list) -> None:
    '''
    Generates a KPOINTS file for a given mesh.

    Parameters
    ----------
    mesh : list
        The mesh to be used.
    '''
    with open('KPOINTS', 'w') as f:
        f.write('Regular {}\t{}\t{} gamma centred mesh\n'.format(*mesh))
        f.write('0\nGamma\n')
        f.write('{}\t{}\t{}\n'.format(*mesh))
        f.write('0 0 0')

def convert_cif(filename: str) -> None:
    '''
    Converts a cif file to a POSCAR file.

    Parameters
    ----------
    filename : str
        The name of the file to be converted.
    '''
    struct = Structure.from_cif(filename)
    struct.write_poscar('POSCAR')


def molecule(filename: str, atom: str, bond_max: float):
    '''
    Finds a molecule in a structure.

    Parameters
    ----------
    filename : str
        The name of the file to be analysed.
    atom : str
        The atom to build the molecule from.
    bond_max : float
        The maximum bond length.
    '''
    struct = Molecule(filename, atom, bond_max)
    struct.find_molecule()


def coord_sphere(filename: str, atom: str, bond_max: float, sphere_num: int):
    '''
    Finds the coordination sphere of a given atom.

    Parameters
    ----------
    filename : str
        The name of structure file
    atom : str
        The central atom
    bond_max : float
        The maximum bond length
    sphere_num : int
        The coordination sphere to be found
    '''
    struct = Molecule(filename, atom, bond_max)
    struct.get_coordination_sphere(sphere_num)
    struct.write_xyz('coord_sphere.xyz')


def write_band(filename: str, dim: list):
    poscar = Structure.from_poscar(filename)
    kpath = poscar.get_kpath()
    path = [kpoint[1] for kpoint in kpath]
    path = [' '.join([str(i) for i in kpoint]) for kpoint in path]
    band_labels = [kpoint[0] for kpoint in kpath]
    band_labels = list(map(lambda x: x.replace('GAMMA', '$\Gamma$'), band_labels))

    with open('band.conf', 'w') as f:
        f.write('ATOM_NAME = {}\n'.format(' '.join(poscar.atoms)))
        f.write('DIM = {} {} {}\n'.format(*dim))
        f.write('BAND = {}\n'.format('  '.join(path)))
        f.write('BAND_LABELS = {}\n'.format(' '.join(band_labels)))

    print('\nK-path written to band.conf')
    print('\tSpacegroup: {}'.format(poscar.spacegroup))
    print('\tAtoms: {}\n'.format(' '.join(poscar.atoms)))
    print('\tk-path:')
    print('\t{}'.format(' -> '.join(band_labels)))
    for kpoint in kpath:
        print('\t{}'.format(kpoint[1]))


def write_mesh(filename: str, dim: list, mesh_points: list):
    poscar = Structure.from_poscar(filename)
    atoms = ' '.join(poscar.atoms)

    with open('mesh.conf', 'w') as f:
        f.write('ATOM_NAME = {}\n'.format(atoms))
        f.write('DIM = {} {} {}\n'.format(*dim))
        f.write('MESH = {} {} {}\n'.format(*mesh_points))


def write_band_dos(filename: str, dim: list, mesh_points: list):
    write_band(filename, dim)
    write_mesh(filename, dim, mesh_points)

    with open('band-pdos.conf', 'w') as f:
        with open('band.conf', 'r') as band:
            f.write(band.read())
        with open('mesh.conf', 'r') as mesh:
            f.write(mesh.readlines()[2])


def reduce(filename, primative, niggli, delaunay, refine):
    struct = Structure.from_poscar(filename)
    cell = struct.reduced_cell(primative, niggli, delaunay, refine)
    struct.coords = cell[1]
    struct.av = cell[0]
    struct.natoms = [list(cell[2]).count(atom) 
                     for atom in list(set(cell[2]))]
    struct.write_poscar('POSCAR_reduced')


def create_input_configurations() -> None:
    '''
    Creates input configurations for VASP calculations.
    '''
    if not os.path.exists(os.path.expanduser('~/.vasp_suite_configs')):
        os.mkdir(os.path.expanduser('~/.vasp_suite_configs'))

    cwd = os.getcwd()
    os.chdir(os.path.expanduser('~/.vasp_suite_configs'))
    with open('relaxation.ini', 'w') as f:
        f.write('''[Relaxation]
prec = ACCURATE
lreal = .FALSE.
lasph = .TRUE.
ismear = 0
sigma = 0.01
nelm = 100
nelmin = 4
ncore = 4
ediff = 1e-08
ediffg = -0.01
ibrion = 2
nsw = 100
isif = 4
potim = 0.5
lwave = .FALSE.
lcharg = .FALSE.
lorbit = 11
gga = PE
ivdw = 11
''')
    with open('scf.ini', 'w') as f:
        f.write('''[SCF]
prec = ACCURATE
lreal = .FALSE.
lasph = .TRUE.
ismear = 0
sigma = 0.01
nelm = 100
nelmin = 4
ncore = 4
ediff = 1e-08
ediffg = -0.01
ibrion = -1
isif = 4
potim = 0.5
lwave = .FALSE.
lcharg = .FALSE.
lorbit = 11
gga = PE
ivdw = 11
''')
    with open('phonon.ini', 'w') as f:
        f.write('''[Phonon]
ALGO = Normal
EDIFF = 1E-8
GGA = PE
ISIF = 2
ISMEAR = 0
LASPH = .TRUE.
LCHARG = .FALSE.
LREAL = .FLASE.
LWAVE = .FALSE.
NSW = 0
PREC = Accurate
SIGMA = 0.01
''')
    os.chdir(cwd)
