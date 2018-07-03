
import numpy as np
import pandas as pd
from ase.io import read as ase_read
from crewp.lodestar.stdout import get_typeinfo

class Orbitals:
    '''
    In Lodestar DFTB infrastructure, 
    indices of physical quantities like: 
      * population on orbitals 'qOrb.dat'
      * PDOS: 'PDOS.orb.###'
    are arranged with atomic orbitals.
    '''
    def __init__(self, genfname, oupfname ):
        # generate orbital MultiIndex
        self.orb_index = self.get_orbital_index(genfname, oupfname)

    def get_orbital_index(self, genfname, oupfname):
        '''
        Get Pandas MultiIndex of orbitals.
        Levels of column-MultiIndex: 
            atom_index(start from 0)
            chemical symbols
            orbital: (s,p,d)
            magnetic quantum numbers: s(0) p(0,1,2) d(0,1,2,3,4)
        '''
        atoms = ase_read(filename=genfname, format='gen')
        chemsymbol_list = atoms.get_chemical_symbols()
        # create hierarchical index for orbital-PDOS table 
        orbital_list = {
                's': [
                        1,      # repetition of chem_symbol in shell_index
                        ['s'],  # append in orbital_index
                        [0],    # append in magnetic_index
                        ],
                'p': [ 
                        4, 
                        ['s']+['p']*3,
                        list(np.concatenate([np.arange(i) for i in [1,3]])),
                        ],
                'd': [ 
                        9,
                        ['s']+['p']*3+['d']*5,
                        list(np.concatenate([np.arange(i) for i in [1,3,5]])),
                        ],
                }
        chemsymbol_dict = get_typeinfo(oupfname) # symbol-max_angular
        atomidx_index = []
        chemsymbol_index = []
        orbital_index = []
        magnetic_index = []
        for i_atom, chem_symbol in enumerate(chemsymbol_list):
            orbital_info = orbital_list[chemsymbol_dict[chem_symbol]]
            atomidx_index += [i_atom]*orbital_info[0]
            chemsymbol_index += [chem_symbol]*orbital_info[0] # currently not used
            orbital_index += orbital_info[1]
            magnetic_index += orbital_info[2]
        orb_index = pd.MultiIndex.from_arrays( [atomidx_index, chemsymbol_index, orbital_index, magnetic_index], )
        orb_index.names = ['AtomID', 'ChemSymbol', 'Orbital', 'AngVec']
        return orb_index

    def read_pdos_df(self, pdosfname='PDOS.orb', ):
        '''
        read PDOS table (resolved to ml quantum number) from PDOS.orb
        '''
        pdos_df = pd.read_csv(
                pdosfname, 
                header=None, 
                index_col=0,
                names=None, 
                delim_whitespace=True, 
                skiprows=[0],
                )
        pdos_df.rename_axis(None, axis=0, inplace=True)
        pdos_df.columns = self.orb_index
        return pdos_df

    def read_orb_pop(self, qorbfname='qOrb.dat'):
        '''
        Read orbital resolved population
        '''
        pop_df = pd.read_csv(
                qorbfname, 
                header=None, 
                skiprows=None,
                index_col=False,
                names=['Population'], 
                usecols=[3],
                delim_whitespace=True, 
                )
        pop_df.index = self.orb_index
        pop_df = pop_df.reset_index()
        pop_df = pd.pivot_table(pop_df, index=['AtomID', 'ChemSymbol',], columns=['Orbital', 'AngVec'], values='Population')
        return pop_df
