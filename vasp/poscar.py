
import numpy as np
from crewp.io.array import read_2darry
from crewp.io.table import read_table

class Poscar:

    def __init__(self, fname='POSCAR'):
        self.fname = fname
        self.read_all()

    def read_all(self):
        poscarf = open(self.fname, 'r')
        self.title = poscarf.readline() # first commentary line
        line = poscarf.readline() # universal scaling
        self.scaling = float(line)
        self.cell = read_2darry(poscarf, 3) # cell vectors (3,3)
        line = poscarf.readline() # same as 'ions per type' in OUTCAR
        self.n_ions = np.array([ int(i) for i in line.split() ])
        line = poscarf.readline()
        tag_char = line.strip()[0]
        if tag_char in ('S', 's'): # Selective dynamics
            line = poscarf.readline()
            coord_constr = read_table(poscarf)
            cols = list(zip(*coord_constr))
            self.coordinates = np.array(cols[:3]).astype(np.float).transpose()
            self.constraint = (np.array(cols[3:]).transpose() == 'T')

    def get_constraint(self):
        return self.constraint

    def get_coordinates(self):
        return self.coordinates
