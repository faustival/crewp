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

def pwchrg_read(inpfname):
    '''
    read the plain text file
    written by :
    /flib/plot_io.f90 subroutine plot_io()

    returns:
    chrg3dary:  order 3 array, axis indexed as (z, y, x)
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
    atom_coord = []
    for i in range(nat):
        words = get_words(inpf)
        print(words)
    # charge density
    chrg1dary = lines2array(inpf,5)
    inpf.close()
    chrg1dary = np.array(chrg1dary)
    if (len(chrg1dary) != nr3*nr2x*nr1x) :
        print('Error with charge density reading, length not match!')
        print('len of charge 1d array',len(chrg1dary))
        sys.exit()
    chrg3dary = chrg1dary.reshape(nr3, nr2x, nr1x)
    print('len of charge 1d array',len(chrg1dary))
    print('shape of charge 3d array',chrg3dary.shape) 
    '''
    Convert cell-vectors and atomic positions to 
    atomic unit, Bohr, charge density grid is set
    with Bohr unit.
    '''
    alat = celldm[0]
    cell = cell*alat
    print(cell)
    return chrg3dary, cell







