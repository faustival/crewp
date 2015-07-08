#! /usr/bin/python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pdos_read import read_pdos

project_dict = { 'Au' : ['s','p','d'],
                 'H'  : ['s'],
                 'O'  : ['s','p'],
               }
# Read surface
workpath = '/home/jinxi/pwjobs/au_surface_proj/au100_lyr17/'
os.chdir(workpath)
filpdos_prefx = 'au100.pdos.plot'
atom_list = list( range(1,7) )
fermi = 7.9929
atm_wfc_lst = []
for id_atom in atom_list:
    atm_wfc_lst.append( ( str(id_atom), 'Au', project_dict['Au'] ) )
engy, pdos = read_pdos(filpdos_prefx, atm_wfc_lst, True, True)
engy = [engy_val - fermi for engy_val in engy]

# Read bulk
workpath = '/home/jinxi/pwjobs/au_surface_proj/au_bulk/'
os.chdir(workpath)
filpdos_prefx = 'au.pdos.plot'
fermi_bulk = 14.6937
atm_wfc_lst = [ ( '1', 'Au', project_dict['Au'] ) ]
engy_bulk, pdos_bulk = read_pdos(filpdos_prefx, atm_wfc_lst, True, True)
engy_bulk = [engy_val - fermi_bulk for engy_val in engy_bulk]



fig = plt.figure()
plot_wfc_list = ['s','p','d']
for wfc in plot_wfc_list:
    ax = fig.add_subplot( 1, len(plot_wfc_list), (plot_wfc_list.index(wfc)+1) )
    for (atom_id, atom, wfc_list) in pdos:
        for wfc_lpdos in wfc_list:
            if wfc_lpdos[0] == wfc:
                ax.plot(wfc_lpdos[1], engy, label=atom_id)
    for (atom_id, atom, wfc_list) in pdos_bulk:
        for wfc_lpdos in wfc_list:
            if wfc_lpdos[0] == wfc:
                ax.plot(wfc_lpdos[1], engy_bulk, label='Bulk')
    ax.legend(loc="lower right", title=wfc)
plt.show()

sys.exit()


