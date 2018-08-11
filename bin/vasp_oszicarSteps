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

# readin OSZICARs from cli 
if len(sys.argv) < 2:
    inpfname = 'OSZICAR'
else:
    inpfname_list = sys.argv[1:]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Steps')
ax.set_ylabel(r'E (eV)')

for inpfname in inpfname_list:
    print('Reading VASP OSZICAR filetype, ', inpfname)
    en_steps = rlx_step(inpfname)
    nstep = en_steps.shape[0]
    step_seq = [i+1 for i in range(nstep)]
    ax.plot(step_seq, en_steps[:,1], label=inpfname)

ax.legend(loc=2)
plt.show()

