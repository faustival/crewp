#! /usr/bin/python3

import os
import sys

workpath = '/home/jinxi/pwjobs/au_surface_proj/au111_lyr5/'
os.chdir(workpath)
inf = open('au111.pdos.plot.pdos_atm#1(Au)_wfc#3(d)', 'r')

def read_pdosf(inpf, spin_pol):
    '''
    INPUT:
        inpf:      input filename, 
        spin_pol:  True for spin-polarized
    OUTPUT:
        engy:      1-dim list, raw energy
        pdos:      If spin-polarized: 
                       [[spin up array],[spin down array]]
                   If not spin-polarized:
                       [pdos array]
    '''
    engy = []
    pdos = []
    if spin_pol:
        pdos.extend([[],[]])
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
                pdos.append( float(words[1]) )
            elif spin_pol:
                pdos[0].append( float(words[1]) )
                pdos[1].append( float(words[2]) )
    return engy, pdos



engy, pdos = read_pdosf(inf, True)

print(pdos)
print(engy)

sys.exit()



