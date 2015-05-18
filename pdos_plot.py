#! /usr/bin/python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pdos_read import read_pdos

workpath = '/home/jinxi/pwjobs/au_surface_proj/au111_lyr5/'
os.chdir(workpath)
filpdos_prefx = 'au111.pdos.plot'
spin_pol = True
sum_spin = True
atom_list = list( range(1,6) )

project_dict = { 'Au' : ['s','p','d'],
                 'H'  : ['s'],
                 'O'  : ['s','p'],
               }

atm_wfc_lst = [
      ('2','Au',['s','p','d'] ),
      ('4','Au',['s','p','d'] ),
    ]

engy, pdos = read_pdos(filpdos_prefx, atm_wfc_lst, spin_pol, sum_spin)


print(pdos)
#print (engy)

fig = plt.figure()
plot_wfc_list = ['s','p','d']
for wfc in plot_wfc_list:
    ax = fig.add_subplot( 1, nwfc, (plot_wfc_list.index(wfc)+1) )
    for (atom_id, atom, wfc_list) in pdos:
        ax.plot



sys.exit()

