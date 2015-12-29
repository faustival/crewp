#! /usr/bin/python3

import numpy as np
from qescripts.atom import Atom

class LDOS:
    '''
    processing LDOS in a single computation, i.e. system sharing same:
    * fermi energy should be naturally the same.
    * energy array

    Two functions:
    * load all LDOS in atomlist, and updated as self.atomlist[i]['ldos']
    * plot ldos
    '''

    def __init__(self, atomlist, fermi):
        '''
        atomlist = [
           {'atomid':13, 'elem':'Pd', 'orbitals':['d'],},
           {'atomid':14, 'elem':'Pd', 'orbitals':['d'],},
                   ]
        '''
        self.atomlist = atomlist
        self.fermi = fermi
        self.getldos()

    def getldos(self):
        '''
        self.atomlist['ldos'] was updated.
        '''
        for atom in self.atomlist:
            atm = Atom(atom['atomid'],atom['elem'])
            atm.get_ldos('plt', atom['orbitals'], readpdos=False, spin=False)
            atom['ldos'] = atm.ldos
        self.enary = self.atomlist[0]['ldos']['enary']

    def plotldos(self, ax, orbital, ls):
        '''
        orbital = 's' / 'p' / 'd'
        '''
        self.ax = ax
        colorlist = ('b', 'r', 'g', 'c', 'm', 'y')
        i = -1
        for atom in self.atomlist:
            i+=1
            color = colorlist[i%len(colorlist)]
            self.ax.plot(self.enary - self.fermi, atom['ldos'][orbital], color = color, label=atom['elem']+' '+str(atom['atomid']), linestyle=ls )

