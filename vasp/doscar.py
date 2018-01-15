
import numpy as np
import pandas as pd

class Doscar:

    def __init__(self, fname='DOSCAR'):
        self.fname = fname
        with open(self.fname, 'r') as f:
            self.nions = int(f.readline().split()[1])
            for i in range(4): # pass these lines
                f.readline()
            words = f.readline().split()
            self.n_energy_grids = int(words[2])
            self.fermi = float(words[3]) 

    def read_dos(self):
        df = pd.read_csv( 
                self.fname, 
                header=None, 
                index_col=0,
                names=['dos', 'intdos'],
                delim_whitespace=True, 
                skiprows = 5+1,
                nrows = self.n_energy_grids,
                )
        self.dos_df = df

    def read_pdos(self):
        '''
        !!!
        Temporarily only shell-resolved!
        Please use LORBIT=10
        !!!
        '''
        # count skip row numbers
        nfrontlines = 5+1+self.n_energy_grids # 5header 1header_of_TDOS 
        skip_rows = [ i for i in range(nfrontlines) ]
        skip_rows += [ ( nfrontlines + (self.n_energy_grids+1)*i_ion ) \
                for i_ion in range(self.nions) ]
        df = pd.read_csv( 
                self.fname, 
                header=None, 
                index_col=0,
                names=['s', 'p', 'd'],
                delim_whitespace=True, 
                skiprows = skip_rows,
                )
        atom_idx = np.concatenate( [ i*np.ones((self.n_energy_grids,), dtype=np.int) for i in range(self.nions) ] )
        df.set_index(atom_idx, append=True, inplace=True)
        df = df.unstack()
        df = df.swaplevel(0, 1, 1).sort_index(1)
        self.pdos_df = df

    def get_dos_df(self):
        if not hasattr(self, 'dos_df'):
            self.read_dos()
        return self.dos_df

    def get_pdos_df(self):
        if not hasattr(self, 'pdos_df'):
            self.read_pdos()
        return self.pdos_df

    def get_fermi(self):
        return self.fermi
