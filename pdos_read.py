#! /usr/bin/python3

import os

workpath = '/home/jinxi/pwjobs/au_surface_proj/au111_lyr5/'
os.chdir(workpath)
inf = open('au111.pdos.plot.pdos_atm#1(Au)_wfc#3(d)', 'r')

def read_pdosf(inpf, spin_pol):
    '''
    input:
      inpf:      input filename, 
      spin_pol:  True for spin-polarized
    output:
      pdos:      
    '''
    pdos = []
    print('initial pdos', pdos)
    while True:
        line = inpf.readline()
        if not line:
            break
        words = line.split()
        if words[0]=='#':
            continue
        else:
            if not spin_pol:
                pdos.append( float(words[1]) )
            elif spin_pol:
                pdos.append( [float(words[1]),float(words[2])] )
    return pdos



pdos = read_pdosf(inf, True)

print(pdos)



