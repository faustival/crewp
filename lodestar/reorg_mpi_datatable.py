
import os
import pandas as pd

def reorg_mpi_df(prefx, col_index=None, skiprows=1, sort_by=[0] ):
    '''
    Read output data-tables ``[prefx].###`` from mpi run, 
    concatenate to single dataframe, 
    sort along ``sort_by`` (default: 1st key).
    '''
    findex=0
    dflist = []
    while True:
        datafname = '{:s}{:03d}'.format(prefx, findex)
        if os.path.isfile(datafname):
            print( 'Reading:  ', datafname )
            df = pd.read_csv( datafname, 
                    header=None, 
                    skiprows=skiprows,
                    names=col_index,
                    delim_whitespace=True, 
                    )
            dflist.append(df)
            findex+=1
        else:
            print( findex, 'files combined.' )
            break
    df_full = pd.concat(dflist)
    # sort by energy value
    df_full.sort_values(by=sort_by, ascending=[True], inplace=True)
    return df_full
