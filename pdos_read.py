#! /usr/bin/python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def read_lpdosf(inpfname, spin_pol):
    '''
    input file structure:
    <beginning of file>
    # E (eV)  ldosup(E)  ldosdw(E) pdosup(E)  pdosdw(E)  ...<$more>
     -6.759  0.944E-07  0.942E-07  0.944E-07  0.942E-07
     ...
     ...
    <end of file>
    <$more> = <more magnetic quantum number>

    INPUT:
        inpf:      input filename, 
        spin_pol:  True for spin-polarized
    OUTPUT:
        engy:      1-dim list, raw energy
        lpdos:      If spin-polarized: 
                       [[spin up array],[spin down array]]
                   If not spin-polarized:
                       [lpdos array]
    '''
    inpf = open(inpfname,'r')
    engy = []
    lpdos = []
    if spin_pol:
        lpdos.extend([[],[]])
    while True:
        line = inpf.readline()
        if not line:
            break
        words = line.split()
        if words[0]=='#':
            continue
        else:
            engy.append( float(words[0]) )
            if not spin_pol:
                lpdos.append( float(words[1]) )
            elif spin_pol:
                lpdos[0].append( float(words[1]) )
                lpdos[1].append( float(words[2]) )
    engy_pts = len(engy)
    inpf.close()
    return engy, lpdos, engy_pts

def read_pdos(file_prefx, atom_wfc_list, spin_pol):
    '''
    [
      ['1','O' ,['s','p']     ],
      ['2','Au',['s','p','d'] ],
      ['4','Au',['s','p','d'] ],
      ...
    ]
    '''
    pdos = []
    orbital_indx = { 's':'1', 'p':'2', 'd':'3', 'f':'4' }
    for atom in atom_wfc_list:
        print(atom)
        for wfc in atom[2]:
            print(wfc)
            lpdos_fname = file_prefx + '.pdos_atm#' + atom[0] + \
                              "(" + atom[1] + ')_wfc#' + \
                              orbital_indx[wfc] + '(' + wfc + ')'
            print(lpdos_fname)

workpath = '/home/jinxi/pwjobs/au_surface_proj/au111_lyr5/'
os.chdir(workpath)
filpdos_prefx = 'au111.pdos.plot'
spin = True
atom_list = list( range(1,6) )

orbital_dict = { 'Au' : ['s','p','d'],
                 'H'  : ['s'],
                 'O'  : ['s','p'],
               }

atm_wfc_lst = [
      ['2','Au',['s','p','d'] ],
      ['4','Au',['s','p','d'] ],
    ]

read_pdos(filpdos_prefx, atm_wfc_lst, spin)



sys.exit()

