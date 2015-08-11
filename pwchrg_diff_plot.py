#! /usr/bin/python3

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from plotio_read import PlotIORead
from chrg_avgz import ChrgAvgZ
from slab_indchrg import SlabIndChrg

'''
Sequence of charge density list:
    total, d, free
'''
#os.chdir(workpath)

rootpath = '/home/jinxi/pwjobs/'
workpathlist = [ 

                [ 'ag111f000_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
                [ 'ag111f010_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
                [ 'ag100f000_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
                [ 'ag100f010_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
                [ 'ag110f000_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
                [ 'ag110f010_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \

#                [ 'au111f000_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
#                [ 'au111f010_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
#                [ 'au100f000_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
#                [ 'au100f010_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \

#                [ 'pt111f000_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
#                [ 'pt111f010_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
#                [ 'pt100f000_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
#                [ 'pt100f010_ncpp/'  , ['chrgsum_060','chrgsum_035'] ] , \
               ]

'''
avgchrglist = 
[  [avg_total, avg_d, avg_free, zaxis ] ,
...
]
'''
avgchrglist = []
zatomlist = []
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
        slabchrg = ChrgAvgZ(chrg3d, cell)
        avgchrg = slabchrg.xyavg()#*slabchrg.xyarea()
        avgchrg_plot.append(avgchrg)
        #print('charge integrated, ', slabchrg.intgrl_z())
    # calculate the free density average line
    avgchrg_plot.append(avgchrg_plot[0] - avgchrg_plot[1])
    # get z-position of atom layers
    atom_coord = chrgdata.atom_coord
    zatom = slabchrg.zatompos(atom_coord, .0001)
    print('atomic layer position, ', zatom)
    # calculate z-axis grid
    atom_coord = chrgdata.atom_coord
    # shift coordinate
    maxcoords = np.amax(atom_coord,axis = 0)
    zshift = maxcoords[-1]
    print('z-axis shifted, ', zshift)
    zaxis = slabchrg.zgrid() - zshift
    zatom = zatom - zshift
    avgchrg_plot.append(zaxis)
    zatomlist.append(zatom)
    avgchrglist.append(avgchrg_plot)

# plot average charge 
def plot_avglist(avgchrglist):
    fig1 = plt.figure()
    label_list = [r'Total valence', r'$\rho$ of $d$ band sum', r'Free charge density']
    ax_sum  = fig1.add_subplot( 2, 1, 1)
    ax_diff = fig1.add_subplot( 2, 1, 2) 
    for [avg_total, avg_d, avg_free, zaxis ] in avgchrglist:
        # plot the total and d-electron density
        ax_sum.plot(zaxis, avg_total, label=label_list[0])
        ax_sum.plot(zaxis, avg_d, label=label_list[1])
        # plot the free-electron density
        ax_diff.plot(zaxis, avg_free, label=label_list[2])
    axlist = [ax_sum, ax_diff]
    for ax in axlist:
        ax.legend(loc=1)
        ax.set_ylabel(r'$\rho(z)$',size=20)
        ax.set_xlabel(r'$z$ ($\AA$)',size=20)
        ax.set_xlim([-20., 10.])
        for zlayer in zatom:
            ax.axvline(x=zlayer,linewidth=2,linestyle='--',color='red')
    plt.show()

def plot_fld_diff(diffchrglist,imgplanelist):
    label_list = [r'Total valence', r'$\rho$ of $d$ band sum', r'Free charge density']
    fig2 = plt.figure()
    ax_tot  = fig2.add_subplot( 2, 1, 1)
    ax_d    = fig2.add_subplot( 2, 1, 2)
    #ax_free = fig2.add_subplot( 3, 1, 3)
    for [ tot, d, free, zaxis ] in diffchrglist:
        ax_tot.plot(zaxis, tot, label=label_list[0])
        ax_d.plot(zaxis, d, label=label_list[1])
        ax_d.plot(zaxis, free, label=label_list[2])
    axlist = [ax_tot, ax_d]
    for ax in axlist:
        ax.legend(loc=1)
        ax.set_ylabel(r'$\rho(z)$',size=20)
        ax.set_xlabel(r'$z$ ($\AA$)',size=20)
        ax.set_xlim([-20., 10.])
        for zlayer in zatom:
            ax.axvline(x=zlayer,linewidth=2,linestyle='--',color='red')
        for zimg in imgplanelist:
            ax.axvline(x=zimg, linewidth=2,linestyle='--')#,color='green')
    plt.show()

# difference charge with field
def diffld(avgchrglist, ncurve):
    def diffchrg(chrgf, chrg0):
        '''
        chrgf, chrg0 =  
        [avg_total, avg_d, avg_free, zaxis ] 
        '''
        diffchrg = []
        for i in range(3):
            slabind = SlabIndChrg(chrgf[i], chrg0[i], chrg0[-1])
            diffchrg.append(slabind.chrgind)
        diffchrg.append(chrg0[-1])
        return diffchrg
    diffchrglist = []
    imgplanelist = []
    for i in range(0,ncurve):
        # calculate charge difference
        diff = diffchrg( avgchrglist[2*i+1] , avgchrglist[2*i] )
        diffchrglist.append(diff)
        # calculate image plane
        slabcenter = .5*(zatomlist[2*i][0] + zatomlist[2*i][-1])
        slabind = SlabIndChrg(avgchrglist[2*i+1][0], avgchrglist[2*i][0], avgchrglist[2*i][-1])
        imgplanelist.append(slabind.imgplane(slabcenter))
    return diffchrglist, imgplanelist

# writing data
for i in range(0,len(avgchrglist)):
    print('avgchrg writing',i)
    data = tuple(avgchrglist[i])
    headtag = ' full_valence     d-valence     free-valence  zaxis'
    np.savetxt('{0:s}{1:s}{2:s}'.format('chrgdiff_',workpathlist[i][0][:-1],'.dat'), np.column_stack(data), header=headtag)

diffchrglist, imgplanelist = diffld(avgchrglist, 3)

plot_avglist(avgchrglist)
plot_fld_diff(diffchrglist,imgplanelist)


