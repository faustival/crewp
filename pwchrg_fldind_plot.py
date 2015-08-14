#! /usr/bin/python3

import os
import numpy as np
import matplotlib.pyplot as plt
from slab_freechrg import SlabFreeChrg


'''
Data from class SlabFreeChrg:

    self.chrgz = [
                  [total, d, free], # 0.0 field
                  [total, d, free], # 1st field
                  ...
                 ]
        
    self.chrgz_diffld = [
                  [total, d, free], # 1st field
                  ...
                 ]
'''
rootpath = '/home/jinxi/pwjobs/'
os.chdir(rootpath)
slablist = [
  { 'elem':'Ag', 'ort':'111', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Ag', 'ort':'100', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Ag', 'ort':'110', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Pt', 'ort':'111', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Pt', 'ort':'100', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Pt', 'ort':'110', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Au', 'ort':'111', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Au', 'ort':'100', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Au', 'ort':'110', 'bands':[60,35], 'flds':[0.0, 0.1] },
           ]

readinlist = [item for item in slablist if item['ort']=='111' ]
#readinlist = [item for item in slablist if item['elem']=='Ag' ]

fig_nofld   = plt.figure()
fig_difffld = plt.figure()
ax_nofld_sum  = fig_nofld.add_subplot(2,1,1)
ax_nofld_free = fig_nofld.add_subplot(2,1,2) 
ax_diff_tot  = fig_difffld.add_subplot(2,1,1)
ax_diff_free = fig_difffld.add_subplot(2,1,2)
axlist = [ax_nofld_sum, ax_nofld_free, ax_diff_tot, ax_diff_free]
ax_nofld = [ax_nofld_sum, ax_nofld_free]
ax_diff = [ax_diff_tot, ax_diff_free]
for slabdict in readinlist:
    print( 'Processing', slabdict['elem'], slabdict['ort'], '...' )
    # get data
    slab = SlabFreeChrg(slabdict)
    slab.zshift_maxlayer()
    slab.set_chrgz_fld()
    slab.set_flddiff()
    slab.set_imgplane()
    # write data file
    slab.wrtdata()
    # plot data, temporarily no field iteration
    ax_nofld_sum.plot(slab.zaxis, slab.chrgz[0][0])
    ax_nofld_sum.plot(slab.zaxis, slab.chrgz[0][1])
    ax_nofld_free.plot(slab.zaxis, slab.chrgz[0][2])
    ax_diff_tot.plot(slab.zaxis, slab.chrgz_diffld[0][0])
    ax_diff_free.plot(slab.zaxis, slab.chrgz_diffld[0][1])
    ax_diff_free.plot(slab.zaxis, slab.chrgz_diffld[0][2])
    for ax in ax_diff:
        for z0 in slab.imgplane:
            ax.axvline(x=z0, linewidth=2,linestyle='--')#,color='green')
    for ax in axlist:
        ax.legend(loc=1)
        ax.set_ylabel(r'$\rho(z)$',size=20)
        ax.set_xlabel(r'$z$ ($\AA$)',size=20)
        ax.set_xlim([0., 10.])
        ax.axvline(x=slab.zatom[-1],linewidth=2,linestyle='--',color='red')
plt.show()



