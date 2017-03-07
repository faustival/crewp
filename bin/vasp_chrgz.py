#! /usr/bin/env python3

import sys
import os
import numpy as np

from crewp.vasp.chgcar import read_chg, read_cell
from crewp.chrg_avgz import ChrgAvgZ
from ase.calculators.vasp import VaspChargeDensity

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
    chrgden = read_chg(fname)
    cell = read_cell(fname)
    chrg_obj = ChrgAvgZ(chrgden, cell)
    chrg_z = chrg_obj.xyavg()
    z_ax = chrg_obj.zgrid()
    return chrg_z, z_ax

# read in CHGCAR filename series from command-line
chrgf_list = sys.argv[1:]

print( sys.version )
print( 'Readin: ', chrgf_list )

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('z (Å)')
ax.set_xlabel(r'$\rho$')

for fname in chrgf_list:
    chrgz, z_ax = get_chrg_avgz(fname)
    ax.plot(z_ax, chrgz, label=fname)

ax.legend(loc=2)
plt.show()




