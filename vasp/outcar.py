
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
    '''
    To keep the information self-consistent, 
    all information was obtained in OUTCAR. 
    I creep over OUTCAR few times,
    because of the messy organization of OUTCAR.
    '''
    def __init__(self, fname):
        self.fname = fname
        self.get_atoms()

    def get_atoms(self):
        elements = []
        outcarf = open(self.fname, 'r')
        '''
        In OUTCAR, header information of POTCAR appeared 2 times,
        and POTCAR elements may have repetition.
        Hence I have introduced: 
        * ``prev_line`` for building correlation between adjacent lines.
        * ``trigger_pseudo`` for judge end of first writing.
        The rule comes: 
        * once trigger_pseudo turned to 'off', it will never be 'on'.
        * the trigger_pseudo was turned 'off', when current line is empty,
          and previous line contains ``POTCAR:``.
        '''
        prev_line = 'noline' 
        trigger_pseudo = 'on'
        while True:
            line = outcarf.readline()
            # find all atomic types
            if 'POTCAR:' in line and trigger_pseudo=='on':
                pseudo_type = line.split()[2]
                m = re.match('[A-Z][a-z]?', pseudo_type)
                elements.append(m.group())
            # determine if the first writing of POTCAR header finished
            if line.strip()=='' and 'POTCAR' in prev_line:
                trigger_pseudo = 'off'
            # how many atoms each type
            if 'ions per type' in line: 
                tmp_str = line.split('=')[1]
                n_ions = [ int(i) for i in tmp_str.split() ]
            '''
            store line string as prev_line for next loop
            Note: always put this on bottom of readline() loop
                  and never ``break`` before this
            '''
            prev_line = line
            if not line: break
        outcarf.close()
        self.elements = elements
        self.n_ions = n_ions

    def get_rx_force(self):
        outcarf = open(self.fname, 'r')
        while True:
            line = outcarf.readline()
            if not line: break
        outcarf.close()



