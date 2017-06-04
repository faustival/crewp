
import numpy as np

def rigid(atoms, idmin, idmax, ):
    '''
    Return a FixInternals object that fix all z-matrix elements from atom idmin to idmax.
    Set the return into:
        ase.constraints.FixInternals( rigid(myatoms, idmax, idmax) )
    '''
    bonds = []
    angles = []
    dihedrals = []
    for iatom in range(idmin, idmax):
        if iatom <= idmax-1: 
            idlist = [iatom, iatom+1]
            bonds.append( [atoms.get_distance(*idlist), idlist] )
        if iatom <= idmax-2:
            idlist = [iatom, iatom+1, iatom+2]
            angles.append( [180./np.pi*atoms.get_angle(idlist), idlist] )
        if iatom <= idmax-3:
            idlist = [iatom, iatom+1, iatom+2, iatom+3]
            dihedrals.append( [180./np.pi*atoms.get_dihedral(idlist), idlist] )
    return bonds, angles, dihedrals


