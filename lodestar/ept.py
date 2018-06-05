
import pandas as pd
from crewp.lodestar.reorg_mpi_datatable import reorg_mpi_df

class ElPhoton:

    def __init__(self):
        pass

    def read_absorption(self):
        df_full = reorg_mpi_df(
                prefx='aCoef.', 
                col_index=['iMode', 'Energy', 'Absorption', 'Emission'],
                skiprows=None,
                sort_by=['Energy'],
                )
        return df_full

