
import sys
import pandas as pd

class Atoms:
    '''
    Generate ``atoms_df``.
    '''

    def __init__( 
            self, 
            ase_atoms=None,
            chemsymbol_list=None, 
            coordinates=None,
            ):
        '''
        Supported ways of initiating ``atoms_df``:
        * Only ase_atoms.
        * chemsymbol_list and coordinates
        '''
        if ase_atoms:
            self.from_ase(ase_atoms)
        elif (chemsymbol_list and coordinates):
            self.gen_atoms_df(chemsymbol_list, coordinates)
        else:
            sys.exit('Generating atoms_df, no proper way found.')

    def gen_atoms_df(self, chemsymbol_list, coordinates):
        chemsymbol_df = pd.DataFrame(chemsymbol_list, columns=['ChemSymbol'])
        coord_df = pd.DataFrame(coordinates, columns=['x', 'y', 'z'])
        self.atoms_df = pd.concat( [chemsymbol_df, coord_df], axis=1)

    def from_ase(self, ase_atoms):
        '''
        Generate from ASE Atoms object.
        '''
        chemsymbol_list = ase_atoms.get_chemical_symbols()
        coordinates = ase_atoms.get_positions()
        self.gen_atoms_df(chemsymbol_list, coordinates)

    def get_atoms_df(self, ):
        return self.atoms_df


