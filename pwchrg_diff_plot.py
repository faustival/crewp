#! /usr/bin/python3

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from pwchrg_read import pwchrg_read
from pwchrg import PWCharge

'''
Sequence of charge density list:
    total, d, free
'''

workpath = '/home/jinxi/pwjobs/ag100f000_ncpp_15layer_2x2'
inpflist = ['chrgsum_350','chrgsum_300']
os.chdir(workpath)

# read in total and d charge densities
chrg3dlist = []
for inpfname in inpflist:
    chrg_in, cell = pwchrg_read(inpfname)
    chrg3dlist.append(chrg_in)
# calculate free electron density
chrg_free = chrg3dlist[0] - chrg3dlist[1]
chrg3dlist.append(chrg_free)

# average densities
avgchrglist = []
for chrg in chrg3dlist:
    chrg3d = PWCharge(chrg, cell, 'ang')
    avgchrg = chrg3d.xyavg()
    print('charge integrated, ',chrg3d.intgrl_z())
    avgchrglist.append(avgchrg)
zaxis = chrg3d.zgrid()

print('free charge integrated, ',chrg3d.intgrl_z())

# writing data
alldata = [zaxis] + avgchrglist
alldata = tuple(alldata)
headtag = 'z-axis    full_valence     d-valence     free-valence'
np.savetxt('chrgden.dat', np.column_stack(alldata), header=headtag)



fig = plt.figure()

label_list = [r'Total valence', r'$\rho$ of $d$ band sum', r'Free charge density']
axlist = []
# plot the total and d-electron density
ax_sum = fig.add_subplot( 2, 1, 1)
for i in range(3):
    ax_sum.plot(zaxis, avgchrglist[i], label=label_list[i])
axlist.append( ax_sum )

# plot the free-electron density
ax_diff = fig.add_subplot( 2, 1, 2) 
ax_diff.plot(zaxis,avgchrglist[2], label=label_list[2])
axlist.append( ax_diff )

for ax in axlist:
    ax.legend(loc=9)
    ax.set_ylabel(r'$\rho(z)$',size=20)
    ax.set_xlabel(r'$z$ ($\AA$)',size=20)
    ax.set_xlim([0.0,cell[2,2]*0.529177])

plt.show()


