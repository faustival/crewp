
import sys
import numpy as np
from crewp.lattice.lattice import cell_volume
from crewp.io.array import read_2darry

def read_chg(fname='CHGCAR'):
    '''
    Read charge density and reshape:
    VASP write CHG and CHGCAR as x-contiguous
    and row-major of numpy was forced to
    reshape as (nz, ny, nx). 
    That is, row(z)-major, column(x)-faster.
    And VASP write rho*cell_volume. See:
    https://cms.mpi.univie.ac.at/vasp/vasp/CHGCAR_file.html
    '''
    chgf = open(fname, 'r')
    for i in range(2): chgf.readline()
    cell = read_2darry(chgf, )
    cell_vol = cell_volume(cell)
    while True: 
        '''
        locating 3 integers and get shape of charge array
        '''
        line = chgf.readline()
        words = line.split()
        if len(words)==3:
            try: 
                chrg_shape = np.array([ int(entry) for entry in words ])
                break # jump out from getting shape
            except ValueError: pass
        if not line: # jump out, cannot get shape
            sys.exit('Reading VASP ', fname, ':\n' \
                    , ', cannot get shape of 3D charge array!')
    chrgden = np.fromfile(chgf, count=np.prod(chrg_shape), sep=' ')
    chrgden = chrgden.reshape(chrg_shape[::-1])
    chrgden /= cell_vol
    chgf.close()
    return chrgden, cell

