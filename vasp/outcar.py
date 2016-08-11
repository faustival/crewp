
import re

class Outcar:
    '''
    To keep the information self-consistent, 
    all information was obtained in OUTCAR. 
    I creep over OUTCAR few times,
    because of the messy organization of OUTCAR.
    '''
    def __init__(self, fname):
        self.fname = fname
        self.get_nions()
        self.get_elements()
        self.get_atomlist()

    def get_nions(self):
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            if 'ions per type' in line: 
                tmp_str = line.split('=')[1]
                n_ionlist = [ int(i) for i in tmp_str.split() ]
                break
        outcarf.close()
        self.n_atoms = sum(n_ionlist)
        self.n_iontype = len(n_ionlist)
        self.n_ionlist = n_ionlist

    def get_elements(self):
        elements = []
        outcarf = open(self.fname, 'r')
        '''
        In OUTCAR, header information of POTCAR appeared 2 times,
        and POTCAR elements may have repetition.
        Hence the end of reading elements from POTCAR info 
        was determined by ``self.n_iontype``.
        '''
        counter = 0
        while counter < self.n_iontype:
            line = outcarf.readline()
            if 'POTCAR:' in line:
                counter += 1
                pseudo_type = line.split()[2]
                m = re.match('[A-Z][a-z]?', pseudo_type)
                elements.append(m.group())
        outcarf.close()
        self.elements = elements

    def get_atomlist(self):
        atomlist = []
        for i, element in enumerate(self.elements):
            atomlist += [element]*self.n_ionlist[i]
        self.atomlist = atomlist

    def get_rlx_traj(self):
        '''
        Read position-vector natom*(3+3) dimensional tuple,
        in ionic relaxation.
        position(3) -- force(3)  
        stored as:
        self.rlx_pos_forc[[[]]] (n_iter*n_atoms*6)
        '''
        outcarf = open(self.fname, 'r')
        rlx_pos_forc = []
        i_rlx = 0
        while True:
            line = outcarf.readline()
            if 'POSITION   ' in line:
                outcarf.readline()
                i_rlx += 1
                pos_forc = []
                i_atom = 0
                while i_atom < self.n_atoms:
                    i_atom += 1
                    line = outcarf.readline()
                    pos_forc.append( [ float(entry) for entry in line.split() ] )
                rlx_pos_forc.append( pos_forc )
            if not line: break
        outcarf.close()
        self.rlx_pos_forc = rlx_pos_forc

    def get_vib(self):
        '''
        Read position-vector natom*(3+3) dimensional tuple,
        in vibrational frequency calculation.
        position(3) - eigenvector of dynamical matrix(3)
        '''
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            if not line: break
        outcarf.close()

    def get_template(self):
        '''
        A template for creeping over OUTCAR line by line
        '''
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            if not line: break
        outcarf.close()



