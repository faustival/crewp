#! /usr/bin/python3

import os
import numpy as np
import matplotlib.pyplot as plt
from slab_freechrg import SlabFreeChrg


'''
Sequence of charge density list:
    total, d, free
'''
rootpath = '/home/jinxi/pwjobs/'
os.chdir(rootpath)
slablist = [
        { 'elem':'Ag', 'ort':'111', 'bands':[60,35] },
        { 'elem':'Ag', 'ort':'100', 'bands':[60,35] },
        { 'elem':'Ag', 'ort':'110', 'bands':[60,35] },
        { 'elem':'Pt', 'ort':'111', 'bands':[60,35] },
        { 'elem':'Pt', 'ort':'100', 'bands':[60,35] },
        { 'elem':'Pt', 'ort':'110', 'bands':[60,35] },
        { 'elem':'Au', 'ort':'111', 'bands':[60,35] },
        { 'elem':'Au', 'ort':'100', 'bands':[60,35] },
        { 'elem':'Au', 'ort':'110', 'bands':[60,35] },
           ]

readinlist = [item for item in slablist if item['ort']=='111' ]
print(readinlist)


fig_nofld   = plt.figure()
fig_difffld = plt.figure()
ax_nofld_sum  = fig_nofld.add_subplot(2,1,1)
ax_nofld_free = fig_nofld.add_subplot(2,1,2) 
ax_diff_tot  = fig_difffld.add_subplot(2,1,1)
ax_diff_free = fig_difffld.add_subplot(2,1,2)
for slabdict in readinlist:
    slab = SlabFreeChrg(slabdict)
    slab.get_flddiff()
    ax_nofld_sum.plot(slab.zaxis, slab.chrgz_nofld[0])
    ax_nofld_sum.plot(slab.zaxis, slab.chrgz_nofld[1])
    ax_nofld_free.plot(slab.zaxis, slab.chrgz_nofld[2])
    ax_diff_tot.plot(slab.zaxis, slab.chrgz_fld[0])
    ax_diff_free.plot(slab.zaxis, slab.chrgz_fld[1])
    ax_diff_free.plot(slab.zaxis, slab.chrgz_fld[2])
plt.show()



