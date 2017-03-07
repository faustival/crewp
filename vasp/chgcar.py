
import sys
import numpy as np
from crewp.io.array import read_2darry

def read_chg(fname='CHGCAR'):
    chgf = open(fname, 'r')
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
    '''
    Read charge density and reshape
    '''
    chrgden = np.fromfile(chgf, count=np.prod(chrg_shape), sep=' ')
    chrgden = chrgden.reshape(chrg_shape[::-1])
    return chrgden

def read_cell(fname='CHGCAR'):
    chgf = open(fname, 'r')
    for i in range(2): chgf.readline()
    cell = read_2darry(chgf, )
    return cell
