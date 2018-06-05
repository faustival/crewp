
import pandas as pd
import csv

def read(fname='TAPE.restartf'):
    '''
    read Mulliken charge from restartf into dataframe
    '''
    mulliken_df = pd.read_csv(
            fname, 
            header=None, 
            skiprows=1,
            names=['AtomID', 'Mulliken'], 
            index_col=0,
            usecols=[0,1],
            delim_whitespace=True, 
            )
    #del mulliken_df.index.name
    return mulliken_df

def write(mulliken_df, fname='TAPE.restartf.NEW', ):
    mulliken_df.to_csv(
            fname, 
            index_label=False,
            header=['   '+str(mulliken_df.shape[0])],
            columns=['Mulliken'], 
            float_format='%20.15f', 
            sep=' ', 
            quoting=csv.QUOTE_NONE, 
            escapechar=" ", 
            )
