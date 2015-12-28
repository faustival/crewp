#! /usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from atom import Atom
from exec_plotdos_funcs import mopdos, moproj

'''
# read pDOS for free molecule
'''
free_fermi = -6.4222
free_en0 = -24.2103
free_path = '/home/jinxi/pwjobs/cyan_ads/cyan_gamma'
free_enary, free_dos, free_sumpdos, free_cyanpdos, free_phenylpdos = mopdos(free_path, free_fermi)
free_enary -= (free_en0 + 2.4919 + 17.49)


'''
# slab projection on molecule
'''
slab_fermi = 2.4919
slab_en0 = -17.49
modosinpf = '/home/jinxi/pwjobs/cyan_ads/au3pd_brg_molproj/plotprojmo.mopdos'
proj_enary, modossum, modosmat = moproj(modosinpf, slab_fermi)
proj_enary -= (slab_en0 + (slab_fermi - slab_en0))


'''
# plot free molecule pdos
'''
#plt.plot(free_enary, free_dos, label='Total DOS')
plt.plot(free_enary, free_cyanpdos,  label='Sum of PDOS on Cyan atoms' )
#plt.plot(free_enary, free_phenylpdos, label='Sum of PDOS on Phenyl atoms' )
plt.plot(free_enary, free_sumpdos, label='Sum of PDOS on all atoms' )

'''
# plot MO projection
'''
plt.plot(proj_enary, modosmat[15], linestyle='--', dashes=(5,1.5), color='b')
plt.plot(proj_enary, modosmat[22], linestyle='--', dashes=(5,1.5), color='r')
#plt.plot(proj_enary, modossum, linestyle='--', dashes=(5,1.5), color='g')

#plt.axvline(x=fermi, linestyle='--', color='k', label='Fermi')
#plt.ylim([0., 2.])
plt.xlim([-11., 7.])
plt.grid()
plt.legend(loc=2)
plt.show()


