
import csv
import numpy as np
import pandas as pd
from crewp.lodestar.restartf import write as write_restartf

class DopingVCA:

    def __init__(self, atoms_df):
        self.atoms_df = atoms_df

    def write_qzerof(self, fname='qzero.inp'):
        vca_chrg_df = pd.DataFrame(self.atoms_df['VCA_Charge'])
        vca_chrg_df = vca_chrg_df[pd.notnull(vca_chrg_df['VCA_Charge'])]
        vca_chrg_df.to_csv(
                fname,
                header=None,
                float_format='%15.10f', 
                sep=' ', 
                quoting=csv.QUOTE_NONE, 
                escapechar=" ", 
                )

    def write_doped_restartf(self, fname='TAPE.restartf.VCAdoped', ):
        mullikendf = pd.DataFrame(self.atoms_df['Mulliken'], columns=['Mulliken'])
        write_restartf(mullikendf, fname=fname, )

    def dope_element(self, chemsym_chrg ):
        '''
        chemsym_density: chemical symbol - VCA charge pair,  
            e.g., ['Si', 0.001]
        '''
        [chemsym, vca_chrg] = chemsym_chrg
        # create VCA_Charge column
        self.atoms_df['VCA_Charge'] = np.nan
        self.atoms_df['VCA_Charge'][ self.atoms_df['Element']==chemsym ] = vca_chrg
        # create Doped Mulliken column
        self.atoms_df['Mulliken'] = self.atoms_df['Mulliken0'] + self.atoms_df.fillna(0.)['VCA_Charge']

