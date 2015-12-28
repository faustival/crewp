#! /usr/bin/python3

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from atom import Atom
from exec_plotdos_funcs import mopdos, moproj

slabdict = {
            'au3pd' :            { 'atmlist': [
                                               {'atomid':15, 'elem':'Pd', 'orbitals':['d'],},
                                              ],
                                   'fermi': 0.9020,
                                 },
            'au3aupd_step05' :   { 'atmlist': [
                                               {'atomid':39, 'elem':'Pd', 'orbitals':['d'],},
                                               {'atomid':40, 'elem':'Pd', 'orbitals':['d'],},
                                               {'atomid':41, 'elem':'Pd', 'orbitals':['d'],},
                                              ],
                                   'fermi': 1.9364,
                                 },
           }

rootdir = '/home/jinxi/pwjobs/cyan_ads/'

fig = plt.figure()
'''
# axis for d band
'''
ax = fig.add_subplot(3,1,1)

for slabdir in slabdict:
    os.chdir(rootdir + slabdir)
    fermi = slabdict[slabdir]['fermi']
    for atom in slabdict[slabdir]['atmlist']:
        atm = Atom(atom['atomid'],atom['elem'])
        atm.get_ldos('plt', atom['orbitals'], readpdos=False, spin=False)
        atom['ldos'] = atm.ldos
        ldos = atom['ldos']
        if slabdir=='au3pd':
            ax.plot( ldos['enary']-fermi, ldos['d'], linestyle='--', dashes=(5,1.5), label=(slabdir+', '+str(atom['atomid'])) )
        else:
            ax.plot( ldos['enary']-fermi, ldos['d'], label=(slabdir+', '+str(atom['atomid'])) )
ax.legend(loc=2)
ax.set_xlim([-11., 7.])
'''
# read pDOS for free molecule
'''
free_fermi = -6.4222
free_en0 = -24.2103
free_path = '/home/jinxi/pwjobs/cyan_ads/cyan_gamma'
free_enary, free_dos, free_sumpdos, free_cyanpdos, free_phenylpdos = mopdos(free_path, free_fermi)
free_enary -= (free_en0 + 2.4919 + 17.49)
'''
# plot free molecule pdos
'''
ax_free = fig.add_subplot(3,1,2)
#ax_free.plot(free_enary, free_dos, label='Total DOS')
ax_free.plot(free_enary, free_cyanpdos,  label='Sum of PDOS on Cyan atoms' )
ax_free.plot(free_enary, free_phenylpdos, label='Sum of PDOS on Phenyl atoms' )
ax_free.plot(free_enary, free_sumpdos, label='Sum of PDOS on all atoms' )

ax_free.legend(loc=2)
ax_free.set_ylim([0., 12.])
ax_free.set_xlim([-11., 7.])

'''
# slab projection on molecule
'''
modosinpf = ['/home/jinxi/pwjobs/cyan_ads/au3pd_brg_molproj/plotprojmo.mopdos', 
             '/home/jinxi/pwjobs/cyan_ads/au3pd_top_molproj/plotprojmo.mopdos']
plotlabel = ['bridge', 'top']
slab_fermi = [ 2.4919, 2.7414 ] # Read from nscf.oup
colorlist = ['b','r','g','y','c']

ax_moproj = fig.add_subplot(3,1,3)
for i in range(len(modosinpf)):
    color = colorlist[i%len(colorlist)]
    proj_enary, modossum, modosmat = moproj(modosinpf[i], slab_fermi[i])
    proj_enary -= slab_fermi[i]
    '''
    # plot MO projection
    '''
    ax_moproj.plot(proj_enary, modosmat[15], linestyle='-', color=color, label='Slab project on $5\sigma$, '+plotlabel[i] )
    ax_moproj.plot(proj_enary, modosmat[22], linestyle='--', dashes=(5,1.5), color=color, label=r'Slab project on $2\pi^{\ast}$, '+plotlabel[i])
#ax_moproj.plot(proj_enary, modossum, linestyle='--', dashes=(5,1.5), color='g')
#ax_moproj.axvline(x=fermi, linestyle='--', color='k', label='Fermi')
ax_moproj.set_ylim([0., 1.])
ax_moproj.set_xlim([-11., 7.])
ax_moproj.legend(loc=2)
ax_moproj.set_xlabel('$\mathrm{E-E_f}$, (eV)',size=22)
for label in ax_moproj.get_xticklabels():
    label.set_color('black')
    label.set_fontsize(22)


plt.show()

