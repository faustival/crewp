#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from plotio_read import PlotIORead
from chrg_avg import ChrgAvg

inpfname = '/home/jinxi/pwjobs/ag100f000_ncpp/chrgsum_60'

# read raw data 
plot_raw = PlotIORead(inpfname, 'ang')
chrg3d = plot_raw.ary3d
cell = plot_raw.cell
atom_coord = plot_raw.atom_coord
print('cell, \n',cell)
print('atomic coordinates, \n',atom_coord)

# do the xy-average
slabchrg = ChrgAvg(chrg3d, cell)
print('charge integrated ',slabchrg.intgrl_z())

avgchrg = slabchrg.xyavg()
zaxis = slabchrg.zgrid()

fig = plt.figure()
ax = fig.add_subplot( 1, 1, 1)
ax.plot(zaxis,avgchrg)
plt.show()


