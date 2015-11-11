#! /usr/bin/python3

import os
import matplotlib.pyplot as plt
from atom import Atom

slabdict = {
            'au3pd' :            { 'atmlist': [
                                               {'atomid':15, 'elem':'Pd', 'orbitals':['d'],},
                                              ],
                                   'fermi': 0.9020,
                                 },
            'au3pd_step0604' :   { 'atmlist': [
                                               {'atomid':33, 'elem':'Pd', 'orbitals':['d'],},
                                               {'atomid':32, 'elem':'Pd', 'orbitals':['d'],},
                                               {'atomid':31, 'elem':'Pd', 'orbitals':['d'],},
                                              ],
                                   'fermi': 0.4466,
                                 },
           }

rootdir = '/home/jinxi/pwjobs/cyan_ads/'

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

for slabdir in slabdict:
    os.chdir(rootdir + slabdir)
    fermi = slabdict[slabdir]['fermi']
    for atom in slabdict[slabdir]['atmlist']:
        atm = Atom(atom['atomid'],atom['elem'])
        atm.get_ldos('plt', atom['orbitals'], readpdos=False, spin=False)
        atom['ldos'] = atm.ldos
        ldos = atom['ldos']
        ax.plot( ldos['enary']-fermi, ldos['d'], label=(slabdir+', '+str(atom['atomid'])) )

ax.legend()
plt.show()



