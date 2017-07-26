
import numpy as np
from crewp.lattice.lattice import frac2cart
from crewp.io.array import read_2darry
from crewp.io.table import read_table

class Poscar:

    def __init__(self, fname='POSCAR'):
        self.fname = fname
        self.read_all()

    def read_all(self):
        poscarf = open(self.fname, 'r')
        self.title = poscarf.readline() # first commentary line
        '''
        # read lattice cell vectors
        '''
        line = poscarf.readline() # universal scaling
        self.scaling = float(line)
        self.cell = read_2darry(poscarf, 3) # cell vectors (3,3)
        self.cell *= self.scaling 
        '''
        # search for number list of atom
        '''
        while True: 
            line = poscarf.readline() 
            try:
                self.n_ions = np.array([ int(i) for i in line.split() ])
                break
            except ValueError:
                pass
        '''
        # search for 'selective' and ('Direct' or 'Cartesian')
        '''
        line = poscarf.readline() 
        if line.strip()[0] in ('S','s'): # Selective dynamics
            self.selectdyn = True
            line = poscarf.readline() # read next line for 'Direct' or 'Cart'
        else:
            self.selectdyn = False
        if line.strip()[0] in ('D','d'):
            self.ifcartesian = False
        elif line.strip()[0] in ('C', 'c', 'K', 'k'):
            self.ifcartesian = True
        '''
        # read coordinate-constraints(3+{3}, natom)
        '''
        coord_constr = read_table(poscarf)
        cols = list(zip(*coord_constr))
        self.coordinates = np.array(cols[:3]).astype(np.float).transpose()
        if not self.ifcartesian:
            self.coordinates = frac2cart( self.coordinates, self.cell )
        if self.selectdyn:
            self.constraint = (np.array(cols[3:]).transpose() == 'T')

    def get_cell(self):
        return self.cell

    def get_constraint(self):
        if not self.selectdyn:
            sys.exit('File ', self.fname, ' has no constraint columns!')
        return self.constraint

    def get_coordinates(self):
        return self.coordinates


