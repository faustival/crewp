
import sys
import re
import numpy as np

class Outcar:
    '''
    To keep the information self-consistent, 
    all information was obtained in OUTCAR. 
    I creep over OUTCAR few times,
    because of the messy organization of OUTCAR.
    '''
    def __init__(self, fname):
        self.fname = fname
        self.read_nions()
        self.read_elements()
        self.gen_atomlist()

    def read_nions(self):
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            if 'ions per type' in line: 
                tmp_str = line.split('=')[1]
                n_ionlist = [ int(i) for i in tmp_str.split() ]
                break
            elif not line: break
        outcarf.close()
        self.n_atoms = sum(n_ionlist)
        self.n_iontype = len(n_ionlist)
        self.n_ionlist = n_ionlist

    def read_elements(self):
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

            elif not line: break
        outcarf.close()
        self.elements = elements

    def gen_atomlist(self):
        atomlist = []
        for i, element in enumerate(self.elements):
            atomlist += [element]*self.n_ionlist[i]
        self.atomlist = atomlist

    '''
    The following methods was not initiated in __init__(self)
    '''

    def read_latvecs(self):
        '''
        Lattice vectors
        '''
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            if 'direct lattice vectors' in line:
                latvecs = []
                for i in range(3):
                    line = outcarf.readline()
                    latvecs.append( [ float(entry) for entry in line.split()[:3] ] )
                break
            elif not line: break
        outcarf.close()
        self.latvecs = latvecs

    def get_rlx_steps(self):
        '''
        Read position-vector natom*(3+3) dimensional tuple,
        in ionic relaxation.
        position(3) -- force(3) (Angstrom -- eV/Angstrom)
        stored as:
        self.rlx_pos3_forc3[[[]]] (n_iter*n_atoms*6)
        '''
        outcarf = open(self.fname, 'r')
        rlx_pos3_forc3 = []
        i_rlx = 0
        while True:
            line = outcarf.readline()
            if 'POSITION   ' in line:
                outcarf.readline()
                i_rlx += 1
                pos_forc = []
                for i_atom in range(self.n_atoms):
                    line = outcarf.readline()
                    pos_forc.append( [ float(entry) for entry in line.split() ] )
                rlx_pos3_forc3.append( pos_forc )
            elif not line: break
        outcarf.close()
        return np.array(rlx_pos3_forc3)

    def get_vib(self):
        '''
        Read position-vector natom*(3+3) dimensional tuple,
        in vibrational frequency calculation.
        position(3) - eigenvector of dynamical matrix(3)
        '''
        outcarf = open(self.fname, 'r')
        # Find number of modes
        while True:
            line = outcarf.readline()
            if 'Degrees of freedom DOF' in line:
                n_modes = int(line.split('=')[-1].split()[0])
                # Find beginning of dynamical matrix
                while True:
                    line = outcarf.readline()
                    if 'Eigenvectors and eigenvalues of the dynamical matrix' in line:
                        for passline in range(3):
                            outcarf.readline() # 3 dummy lines
                        # Get all vibrational info
                        vib_pos3_eigvec3 = []
                        for i_mode in range(n_modes):
                            vib_header = outcarf.readline()
                            print(vib_header)
                            outcarf.readline() # a dummy line
                            # Get eigenvector within single mode
                            pos_eigvec = []
                            for i_atom in range(self.n_atoms):
                                line = outcarf.readline()
                                pos_eigvec.append( [ float(entry) for entry in line.split() ] )
                            outcarf.readline() # a dummy line
                            vib_pos3_eigvec3.append(pos_eigvec)
                        break
            if not line: break # always put this before close file
        outcarf.close() # always put this on bottom of readline loop
        return np.array(vib_pos3_eigvec3)

    '''
    Methods only for return things
    '''

    def get_atomlist(self):
        if not hasattr(self, 'atomlist'):
            self.gen_atomlist()
        return self.atomlist

    def get_latvecs(self):
        if not hasattr(self, 'latvecs'):
            self.read_latvecs()
        return self.latvecs

    def auto_creep(self):
        '''
        Determine type of ionic update by reading ``IBRION``.
        And creep for corresponding components.
        * IBRION in range [1, 3]: call self.get_rlx_steps()
        * IBRION in range [5, 8]: call self.get_vib()
        '''
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            if 'IBRION' in line and '=' in line:
                ibrion = int(line.split('=')[-1].split()[0])
                break
            elif not line: break
        outcarf.close()
        if 0 <= ibrion <= 3:
            anim_vec6d = self.get_rlx_steps() 
        elif 5 <= ibrion <= 8:
            anim_vec6d = self.get_vib()
        else:
            sys.exit('No IBRION match, auto_creep stop running.')
        return ibrion, anim_vec6d

