#! /usr/bin/env python3

import sys
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt
from crewp.vasp.oszicar import rlx_step

mpl.rcParams.update({'font.size': 10,
                     'font.family': "serif",
                     #'font.serif': [],                   
                     #'font.sans-serif': ["DejaVu Sans"], 
                     'mathtext.default' : 'regular',
                    })

if len(sys.argv) < 2:
    inpfname = 'OSZICAR'
else:
    inpfname = sys.argv[1]
print('Reading VASP OSZICAR filetype, ', inpfname)

en_steps = rlx_step(inpfname)
nstep = en_steps.shape[0]
step_seq = [i+1 for i in range(nstep)]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Steps')
ax.set_ylabel(r'E ()')
ax.plot(step_seq, en_steps[:,1])

plt.show()

