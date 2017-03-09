
import numpy as np

def plotio_read(inpfname):
    '''
    read the plain text file
    written by :
    /flib/plot_io.f90 subroutine plot_io()

    returns:
    ary3d:  order 3 array, axis indexed as (z, y, x),
    because of writing in Fortran type.
    '''
    inpf = open(inpfname, 'r')
    # title
    words = inpf.readline().split()
    # grid number, number of atom, number of atomic types
    words = inpf.readline().split()
    nr1x, nr2x, nr3x, nr1, nr2, nr3, nat, ntyp = [int(nu) for nu in words.copy()]
    # ibrav and celldm
    words = inpf.readline().split()
    ibrav = int(words[0])
    celldm = tuple([float(words[i]) for i in range(1,7)])
    if ibrav==0:
        cell = np.zeros((3,3))
        for i in range(3):
            words = inpf.readline().split()
            cellvec = np.array([float(nu) for nu in words])
            cell[i] = cellvec
    # energy cutoff, ...
    words = inpf.readline().split()
    gcutm, dual, ecut = [float(words[i]) for i in range(3)]
    plot_num = int(words[3])
    # atom type list and valence charge
    zvalence = []
    for i in range(ntyp):
        words = inpf.readline().split()
        zval = []
        zval.append(int(words[0]))
        zval.append(words[1])
        zval.append(float(words[2]))
        zval = tuple(zval)
        zvalence.append(zval)
    # atomic positions
    atom_coord = np.zeros((nat,3))
    for i in range(nat):
        words = inpf.readline().split()
        atm = np.array([float(nu) for nu in words[1:4]])
        atom_coord[i] = atm
    # 3d array quantities, e.g. charge density, written as '(5(1pe17.9))'
    ary1d = np.fromfile(inpf, count=nr3*nr2x*nr1x, sep=' ')
    ary3d = ary1d.reshape(nr3, nr2x, nr1x)
    inpf.close()
    '''
    Convert cell-vectors and atomic positions to 
    atomic unit, Bohr, 3-Dim grid is set
    with Bohr unit.
    '''
    alat = celldm[0]
    cell = cell*alat
    atom_coord = atom_coord*alat
    return ary3d, cell, atom_coord

class PlotIORead:
    '''
    Containing:
     * PW Charge
    and related properties:
     * cell vectors
     * atomic positions
    Default in Bohr unit.
    '''
    def __init__(self, inpfname, unit='bohr'):
        # save all from raw data file
        ary3d, cell, atom_coord \
        = plotio_read(inpfname)

        # transform to angstrom unit, if need
        bohr2ang = 0.529177
        if unit=='ang':
            ary3d = ary3d/bohr2ang**3
            cell = cell*bohr2ang
            atom_coord = atom_coord*bohr2ang
        self.ary3d      = ary3d
        self.cell       = cell
        self.atom_coord = atom_coord 




