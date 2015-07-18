#! /usr/bin/python3

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from plotio_read import PlotIORead
from chrg_avg import ChrgAvg

'''
Sequence of charge density list:
    total, d, free
'''
#os.chdir(workpath)

rootpath = '/home/jinxi/pwjobs/'
workpathlist = [ [ 'ag100f000_ncpp_15layer_2x2/', ['chrgsum_350','chrgsum_300'] ] , \
                 [ 'ag100f000_ncpp_15layer/'    , ['chrgsum_100','chrgsum_075'] ] , \
                 [ 'ag100f000_ncpp/'            , ['chrgsum_60','chrgsum_35'] ] , \
               ]

'''
avgchrglist = 
[  [avg_total, avg_d, avg_free, zaxis ] ,
...
]
'''
avgchrglist = []
for [workpath, flist] in workpathlist:
    avgchrg_plot = []
    for fname in flist:
        # read the raw data file
        inpfname = rootpath + workpath + fname
        print('Reading... ', inpfname)
        chrgdata = PlotIORead(inpfname, 'ang')
        chrg3d = chrgdata.ary3d
        cell = chrgdata.cell
        # calculate the average density
        slabchrg = ChrgAvg(chrg3d, cell)
        avgchrg = slabchrg.xyavg()
        avgchrg_plot.append(avgchrg)
        print('charge integrated, ', slabchrg.intgrl_z())
    # calculate the free density average line
    avgchrg_plot.append(avgchrg_plot[0] - avgchrg_plot[1])
    # calculate z-axis grid
    atom_coord = chrgdata.atom_coord
    maxcoords = np.amax(atom_coord,axis = 0)
    zshift = maxcoords[-1]
    print('z-axis shifted, ', zshift)
    zaxis = slabchrg.zgrid() - zshift
    avgchrg_plot.append(zaxis)
    avgchrglist.append(avgchrg_plot)

## writing data
#alldata = [zaxis] + avgchrglist
#alldata = tuple(alldata)
#headtag = 'z-axis    full_valence     d-valence     free-valence'
#np.savetxt('chrgden.dat', np.column_stack(alldata), header=headtag)

# plot 
fig = plt.figure()

label_list = [r'Total valence', r'$\rho$ of $d$ band sum', r'Free charge density']
ax_sum  = fig.add_subplot( 2, 1, 1)
ax_diff = fig.add_subplot( 2, 1, 2) 
for [avg_total, avg_d, avg_free, zaxis ] in avgchrglist:
    # plot the total and d-electron density
    ax_sum.plot(zaxis, avg_total, label=label_list[0])
    ax_sum.plot(zaxis, avg_d, label=label_list[1])
    # plot the free-electron density
    ax_diff.plot(zaxis, avg_free, label=label_list[2])

axlist = [ax_sum, ax_diff]

for ax in axlist:
    ax.legend(loc=9)
    ax.set_ylabel(r'$\rho(z)$',size=20)
    ax.set_xlabel(r'$z$ ($\AA$)',size=20)
    #ax.set_xlim([0.0,cell[2,2]*0.529177])

plt.show()


