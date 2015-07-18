#! /usr/bin/python3

import numpy as np
import sys

def get_words(inpf):
    line = inpf.readline()
    return line.split()

def lines2array(inpf,ncol):
    arry = []
    while True:
        words = get_words(inpf)
        if len(words)>ncol:
            print('RESET the column number!')
            break
        elif len(words)<ncol:
            rowary = [float(num) for num in words]
            arry += rowary
            break
        else:
            rowary = [float(num) for num in words]
            arry += rowary
    return arry

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
    words = get_words(inpf)
    # grid number, number of atom, number of atomic types
    words = get_words(inpf)
    nr1x, nr2x, nr3x, nr1, nr2, nr3, nat, ntyp = [int(nu) for nu in words.copy()]
    # ibrav and celldm
    words = get_words(inpf)
    ibrav = int(words[0])
    celldm = tuple([float(words[i]) for i in range(1,7)])
    if ibrav==0:
        cell = np.zeros((3,3))
        for i in range(3):
            words = get_words(inpf)
            cellvec = np.array([float(nu) for nu in words])
            cell[i] = cellvec
    # energy cutoff, ...
    words = get_words(inpf)
    gcutm, dual, ecut = [float(words[i]) for i in range(3)]
    plot_num = int(words[3])
    # atom type list and valence charge
    zvalence = []
    for i in range(ntyp):
        words = get_words(inpf)
        zval = []
        zval.append(int(words[0]))
        zval.append(words[1])
        zval.append(float(words[2]))
        zval = tuple(zval)
        zvalence.append(zval)
    print(zvalence)
    # atomic positions
    atom_coord = np.zeros((nat,3))
    for i in range(nat):
        words = get_words(inpf)
        atm = np.array([float(nu) for nu in words[1:4]])
        atom_coord[i] = atm
    # 3d array quantities, e.g. charge density, written as '(5(1pe17.9))'
    ary1d = lines2array(inpf,5)
    inpf.close()
    ary1d = np.array(ary1d)
    if (len(ary1d) != nr3*nr2x*nr1x) :
        print('Error with 3-Dim array reading, length not match!')
        print('len of 1-Dim array',len(ary1d))
        sys.exit()
    ary3d = ary1d.reshape(nr3, nr2x, nr1x)
    print('len of 1-Dim array',len(ary1d))
    print('shape of 3-Dim array',ary3d.shape) 
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





