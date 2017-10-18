#! /usr/bin/env python3

import numpy as np

import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt

mpl.rcParams.update({'font.size': 10,
                     'font.family': "serif",
                     #'font.serif': [],                   
                     #'font.sans-serif': ["DejaVu Sans"], 
                     'mathtext.default' : 'regular',
                    })

enstep_fname = 'WATER-1.ener'

cols = np.loadtxt(enstep_fname, unpack=True)

#print(*(cols[1:6].tolist()))
timestep, kineticstep, tempstep, potstep, consstep = cols[1:6].tolist()

print(timestep)
print(kineticstep)


fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(timestep, consstep, label='Kinetic')

ax.legend(loc=2)
plt.show()



