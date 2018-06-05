
import numpy as np
import pandas as pd
from ase.io import read as ase_read
from crewp.lodestar.stdout import get_typeinfo

def read_pdos_df(genfname, oupfname, pdosfname='PDOS.orb', ):
    '''
    read PDOS table (resolved to ml quantum number) from PDOS.orb

        Levels of column-MultiIndex: 
            atom_index(start from 0)
            chemical symbols
            orbital: (s,p,d)
            magnetic quantum numbers: s(0) p(0,1,2) d(0,1,2,3,4)
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
    col_index = pd.MultiIndex.from_arrays( [atomidx_index, chemsymbol_index, orbital_index, magnetic_index], )
    pdos_df.columns = col_index
    return pdos_df

