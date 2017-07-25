#! /usr/bin/env python3

import sys
import numpy as np
from crewp.vasp.poscar import Poscar
from crewp.vasp.outcar import Outcar
from crewp.io.array import wrt_2darry

logf = sys.stdout

# first sysarg should be OUTCAR with atom list
outcar = Outcar(sys.argv[1])
atomlist = atomlist = outcar.get_atomlist()

fnamelist = sys.argv[2:]

# stack coordinates from CONTCARs
coordlist = []
for fname in fnamelist:
    contcar = Poscar(fname)
    coordinates = contcar.get_coordinates()
    constraint = contcar.get_constraint()
    constraint[ constraint ] == 0.
    coordinates *= constraint
    coordlist.append( coordinates )

# concatenate into coordinate table
coord_table = coordlist[0]
for i in range(np.shape(coordlist)[0]-1):
    coord_table = np.concatenate( (coord_table, coordlist[i+1]), axis=1 )

wrt_2darry(coord_table, title='', rowtags=atomlist, f=logf)

