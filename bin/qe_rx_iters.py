#! /usr/bin/env python3

import sys
import re
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt
from qescripts.qe.rxiters import rxIters

plt.rc('text', usetex=True)
globfontsize = 26
mpl.rcParams.update({'font.size': globfontsize,
                     'font.family': "serif",
                     #'font.serif': [],                   
                     #'font.sans-serif': ["DejaVu Sans"], 
                     'mathtext.default' : 'regular',
                    })

rxoupf = sys.argv[1]

iterobj = rxIters(rxoupf)
iterobj.rxconv()
iterobj.printconv()

fig = plt.figure()
ax_forc = fig.add_subplot(2,1,1)
ax_en = fig.add_subplot(2,1,2)
ax_forc.set_ylabel('Total force, (Ry/a.u.)')
ax_en.set_ylabel('$\Delta$E, (Ry)')
ax_en.set_xlabel('Iteration steps in optimization')

ax_en.plot(iterobj.iterseq, iterobj.endiff,'o-')
ax_forc.plot(iterobj.iterseq, iterobj.forcseq,'o-')
for ax in (ax_en,ax_forc):
    ax.set_xlim(1,iterobj.iterseq[-1])
#ax_forc.set_ylim(0.0, 0.005)
ax_en.set_ylim(-0.0001, 0.0001)
plt.show()



