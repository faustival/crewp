
import sys
import numpy as np

class SKF:
    '''
    See SKF file format description:
    <https://www.dftb.org/fileadmin/DFTB/public/misc/slakoformat.pdf>
    '''

    def __init__(self, fname):
        self.fname = fname
        self.orbtags = [ 'Hdd0', 'Hdd1', 'Hdd2', 'Hpd0', 'Hpd1', 'Hpp0', 'Hpp1', 'Hsd0', 'Hsp0', 'Hss0', 'Sdd0', 'Sdd1', 'Sdd2', 'Spd0', 'Spd1', 'Spp0', 'Spp1', 'Ssd0', 'Ssp0', 'Sss0',]

    def read_simple(self):
        self.skf = open(self.fname)
        line = self.skf.readline() # 1st line
        w1, w2 = line.split()
        self.griddist = float(w1)
        self.ngpoints = int(w2)
        self.rcut = self.griddist*float(self.ngpoints)
        line = self.skf.readline() # 2nd line missed
        line = self.skf.readline() # 3rd line missed
        intmat = []
        for i in range(self.ngpoints): # H and S matrix table
            words = self.skf.readline().split() 
            row = []
            for a in words:
                try:
                    row.append(float(a))
                except ValueError: # repeat*val format
                    repeat, val = a.split('*')
                    row += [ float(val) ]*int(repeat)
            intmat.append( row )
        self.intmat = np.array(intmat).transpose()
        self.skf.close()

    def set_rseq(self):
        '''
        Generate array of radius grid.
        Note: start point, R=0. is not included, endpoint is included. 
        See Line 4 explaination, simple Homo-nuclear case, SKF format description. 
        '''
        self.rseq = np.linspace(self.griddist, self.rcut, self.ngpoints)

    def get_int_table(self, inttag='', ):
        if not inttag: # default
            return self.intmat
        else:
            #try:
            irow = self.orbtags.index(inttag)
            return self.intmat[irow]
                #sys.exit('In SKF.get_int_table: inttag should be in orbtags list!')

    def get_rseq(self):
        if not hasattr(self, 'rseq'):
            self.set_rseq()
        return self.rseq
