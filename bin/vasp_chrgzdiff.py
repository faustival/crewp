#! /usr/bin/env python3

import sys
import os
import numpy as np

from crewp.vasp.chgcar import read_chg
from crewp.chrg_avgz import ChrgAvgZ

import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt

mpl.rcParams.update({'font.size': 10,
                     'font.family': "serif",
                     #'font.serif': [],                   
                     #'font.sans-serif': ["DejaVu Sans"], 
                     'mathtext.default' : 'regular',
                    })

def get_chrg_avgz(fname):
    chrgden, cell = read_chg(fname)
    chrg_obj = ChrgAvgZ(chrgden, cell)
    chrg_z = chrg_obj.xyavg()
    z_ax = chrg_obj.zgrid()
    return chrg_z, z_ax

# read in CHGCAR filename series from command-line
chrgf_list = sys.argv[1:]

print( sys.version )
print( 'Readin: ', chrgf_list )

# get the basis charge for differences

chrg_z0, zaxis = get_chrg_avgz(chrgf_list[0])

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('z (Å)')
ax.set_ylabel(r'$\Delta \rho$')

for fname in chrgf_list[1:]:
    chrgz, z_ax = get_chrg_avgz(fname)
    diff_chrgz = chrgz - chrg_z0
    ax.plot(zaxis, diff_chrgz, label=fname)

ax.legend(loc=2)
plt.show()




