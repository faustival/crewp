#! /usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from atom import Atom


'''
# sum atomic PDOS
'''
def sumatompdos(atmidlist, atmlist):
    '''
    # iterating over required atomic id-list
    '''
    for atomid in atmidlist:
        idstr = str(atomid)
        atomdict = atmlist[idstr] 
        atom = Atom(idstr,atomdict['elem'])
        atom.get_ldos('plt', atomdict['orbitals'], readpdos=False, spin=False)
        # compute sum of atomic orbital PDOS
        arylen = atom.ldos['enary'].shape[0]
        atomdict['ldos_tot'] = np.zeros((arylen))
        for orbitalkey in atomdict['orbitals']:
            atomdict['ldos_tot'] += atom.ldos[orbitalkey]
    sumpdos = np.zeros((arylen))
    for atomid in atmidlist:
        sumpdos += atmlist[str(atomid)]['ldos_tot']
    pdos_enary = atom.ldos['enary']
    return  pdos_enary, sumpdos

'''
# sum pdos of molecule
'''
def mopdos(datapath, fermi):
    os.chdir(datapath)
    # read total DOS
    cols = np.loadtxt('dos.plt', unpack=True)
    enary = cols[0]
    dos = cols[1]
    '''
    # build total atomic dictionary
    '''
    # initial list for NC function group
    atmlist = {
                '12' :{'elem':'N', 'orbitals':['s','p'],},
                '13' :{'elem':'C', 'orbitals':['s','p'],},
                }
    # append C and H on benzene
    for i in range(1,7):
        idstr = str(i)
        atmlist[idstr] = {'elem':'C', 'orbitals':['s','p'],}
    for i in range(7,12):
        idstr = str(i)
        atmlist[idstr] = {'elem':'H', 'orbitals':['s'],}
    # assign atomic list
    cyanlist = [12,13]
    phenyllist = [i for i in range(1,12)]
    totlist = [i for i in range(1,14)]
    # sum pdos of all atoms
    enary, sumpdos = sumatompdos(totlist, atmlist)
    # sum of cyan groups
    enary, cyanpdos = sumatompdos(cyanlist, atmlist)
    # sum of phenyl groups
    enary, phenylpdos = sumatompdos(phenyllist, atmlist)
    # shift fermi energy
    #enary -= fermi
    return enary, dos, sumpdos, cyanpdos, phenylpdos

'''
# MO projection
'''
def moproj(inpf, fermi):
    nstate = 40
    modosdata = pd.read_csv(inpf, delim_whitespace=True, comment='#', index_col=0, header=None, names=['engy','dos'])
    # reform this use Hierarchical indexing and Reshaping 
    modosmat = [modosdata.ix[i]['dos'].values for i in range(1,nstate+1)]
    modossum = np.zeros((modosmat[0].shape[0]))
    for dos in modosmat:
        modossum += dos
    # shift fermi energy
    enary = modosdata.ix[1]['engy'].values
    #enary -= fermi
    return enary, modossum, modosmat


