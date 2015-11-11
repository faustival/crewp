#! /usr/bin/python3

import os
from atom import Atom

slablist = { 'au3pd'   : [ {'atomid':12, 'elem':'Au', 'orbitals':['d','s'],},
                           {'atomid':13, 'elem':'Pd', 'orbitals':['d'],},
                         ],
             'au4_top' : [ {'atomid':16, 'elem':'Au', 'orbitals':['d'],},
                           {'atomid':17, 'elem':'C' , 'orbitals':['s','p'],},
                         ],
           }

rootdir = '/home/jinxi/pwjobs/cyan_ads/'

for slabdir in slablist:
    os.chdir(rootdir + slabdir)
    for atom in slablist[slabdir]:
        atm = Atom(atom['atomid'],atom['elem'])
        atm.get_ldos('plt', atom['orbitals'], readpdos=False, spin=False)



