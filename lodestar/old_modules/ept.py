
import sys
import os
import csv
import numpy as np
import pandas as pd

def sum_kpts():
    eptf_prefx = "elecPhoton.dat."
    '''
    # read all k-resolved datasets, concatenate into one 
    '''
    findex = 0
    dflist = []
    while True:
        eptfname = '{:s}{:03d}'.format(eptf_prefx,findex)
        if os.path.isfile(eptfname):
            print('Reading:  ', eptfname)
            df_proc = pd.read_csv( 
                    eptfname, 
                    header=None, 
                    skiprows=1,
                    names=['KPoints', 'Energy', 'Absorption', 'Emission'],
                    delim_whitespace=True, 
                    usecols=[0, 1, 4, 5],
                    )
            dflist.append(df_proc)
            findex+=1
        else:
            print(findex, 'files concatenated.')
            break
    df = pd.concat(dflist)
    '''
    # kept for check summation 
    test_en_pt = 0.37246
    df_single_en = df.loc[ df['Energy']==test_en_pt , :].copy() 
    df_single_en.sort_values(by=['KPoints'], ascending=[True], inplace=True)
    absorption_arry = df_single_en['Absorption'].values
    print('Absorption array (for different k-points): \n', absorption_arry)
    print('Absorption summed over k-points: \n', np.sum(absorption_arry))
    #'''
    '''
    # group and sum over k-points by Energy
    '''
    grouped = df.iloc[:,:].groupby(df['Energy'])
    df_sumk = grouped.sum()
    '''
    # kept for check summation 
    print( df_sumk.loc[ test_en_pt ] )
    #'''
    return df_sumk

