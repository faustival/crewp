#! /usr/bin/env python3

import sys
import os
import numpy as np

import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt

from crewp.middleware.chrgden import get_chrg_avgz

mpl.rcParams.update({'font.size': 10,
                     'font.family': "serif",
                     #'font.serif': [],                   
                     #'font.sans-serif': ["DejaVu Sans"], 
                     'mathtext.default' : 'regular',
                    })

# read in CHGCAR filename series from command-line
packname = sys.argv[1]
chrgf_list = sys.argv[2:]

print( sys.version )
print( 'Readin: ', chrgf_list )

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('z (Å)')
ax.set_ylabel(r'$\rho$')

for fname in chrgf_list:
    chrgz, z_ax = get_chrg_avgz(fname, packname)
    ax.plot(z_ax, chrgz, label=fname)
    print( '    '+fname, ' done.')

ax.legend(loc=2)
plt.show()

