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
  { 'elem':'Pt-H', 'ort':'111', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Pt-H-Sym', 'ort':'111', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Pt', 'ort':'100', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Pt', 'ort':'110', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Au', 'ort':'111', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Au', 'ort':'100', 'bands':[60,35], 'flds':[0.0, 0.1] },
  { 'elem':'Au', 'ort':'110', 'bands':[60,35], 'flds':[0.0, 0.1] },
           ]

readinlist = [item for item in slablist if item['ort']=='111' ]
#readinlist = [item for item in slablist if item['elem']=='Ag' ]
plotxlim = [-20., 5.]
colorlist = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
labelfontsize = 30

# creat figures
fig_nofld   = plt.figure()
fig_difffld = plt.figure()
# list figure combinations
figlist = [fig_nofld, fig_difffld]
# create subplots
ax_nofld_sum  = fig_nofld.add_subplot(2,1,1)
ax_nofld_free = fig_nofld.add_subplot(2,1,2) 
ax_diff_tot  = fig_difffld.add_subplot(2,1,1)
ax_diff_free = fig_difffld.add_subplot(2,1,2)
# list axes combinations
axlist = [ax_nofld_sum, ax_nofld_free, ax_diff_tot, ax_diff_free]
ax_nofld = [ax_nofld_sum, ax_nofld_free]
ax_diff = [ax_diff_tot, ax_diff_free]
imgplane_list = []
counter = -1
for slabdict in readinlist:
    print( 'Processing', slabdict['elem'], slabdict['ort'], '...' )
    counter += 1
    # get data
    slab = SlabFreeChrg(slabdict)
    # shift to align
    if slab.elem=='Pt-H':
        slab.zshift_layer(1)
    elif slab.elem=='Pt-H-Sym':
        slab.zshift_layer(1)
    else:
        slab.zshift_layer(0)
    print('atomic layers', slab.zatom)
    slab.set_chrgz_fld()
    slab.set_flddiff()
    # compute the imageplane for different center reference
    if slab.elem=='Pt-H':
        slab.set_imgplane([1,-1])
    if slab.elem=='Pt-H-Sym':
        slab.set_imgplane([1,-2])
    else:
        slab.set_imgplane([0,-1])
    imgplane_list.append(slab.imgplane)
    # write data file
    slab.wrtdata()
    # plot data, temporarily no field iteration
    color = colorlist[counter % len(colorlist)]
    legend_pref = slab.elem + slab.ort
    ax_nofld_sum.plot(slab.zaxis, slab.chrgz[0][0], color=color, label=legend_pref+' Total')
    ax_nofld_sum.plot(slab.zaxis, slab.chrgz[0][1], color=color, linestyle='--', dashes=(5,1.5), label=legend_pref+' $d$')
    ax_nofld_free.plot(slab.zaxis, slab.chrgz[0][2], color=color, label=legend_pref+' Free')
    # 
    ax_diff_tot.plot(slab.zaxis, -slab.chrgz_diffld[0][0], color=color, label=legend_pref+' Total')
    ax_diff_free.plot(slab.zaxis, -slab.chrgz_diffld[0][1], color=color, linestyle='--', dashes=(5,1.5), label=legend_pref+' $d$')
    ax_diff_free.plot(slab.zaxis, -slab.chrgz_diffld[0][2], color=color, label=legend_pref+' Free')
    # all axes
    for ax in axlist:
        ax.legend(loc=1)
        ax.set_xlabel(r'$z$ ($\AA$)',size=labelfontsize)
        ax.set_xlim(plotxlim)
        #for atompos in slab.zatom:
        #    ax.axvline(x=atompos,linewidth=1,linestyle='-',color=color)
    # axis of 0-field charge
    for ax in ax_nofld:
        ax.set_ylabel(r'$\rho(z)$',size=labelfontsize)
    # axis of field difference
    for ax in ax_diff:
        ax.set_ylabel(r'$\Delta\rho(z)$',size=labelfontsize)
        for z0 in slab.imgplane:
            ax.axvline(x=z0, color=color, linewidth=1, linestyle='--')
print('List of image plane, ', imgplane_list)
for fig in figlist:
    fig.subplots_adjust(left=0.07, right=0.98, top=0.95, bottom=0.1)
plt.show()



