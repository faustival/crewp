
import re

def read_pos_vec():
    '''
    Read position-vector natom*(3+3) dimensional tuple,
    used in:
    * ionic relaxation: position(3) - force(3)  
    * frequency: position(3) - eigenvector of dynamical matrix(3)
    '''
    pass

class Outcar:
    def __init__(self, fname):
        self.fname = fname

    def get_basics(self):
        elements = []
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            # find all atomic types
            if 'POTCAR' in line: 
                source = line.split()[2]
                m = re.match('[A-Z][a-z]?', source)
                if m and m.group() not in elements:
                    elements.append(m.group())
                    print(m.group())
                elif len(elements)>0 and m.group() in elements:
                    pass
            # how many atoms each type
            if 'ions per type' in line: 
                pass
            if not line: break
        outcarf.close()

    def get_rx_force(self):
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            if not line: break
        outcarf.close()



