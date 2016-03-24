#! /usr/bin/python3

import numpy as np
from qescripts.atom import Atom

class PDOS:
    '''
    processing PDOS in a single computation, i.e. system sharing same:
    * fermi energy should be naturally the same.
    * energy array

    Two functions:
    * load all PDOS in atomlist, and updated as self.atomlist[i]['pdos']
    * plot pdos
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
        self.getpdos()

    def getpdos(self):
        '''
        self.atomlist['pdos'] was updated.
        '''
        for atom in self.atomlist:
            atm = Atom(atom['atomid'],atom['elem'])
            atm.get_pdos('plt', atom['orbitals'], readpdos=False, spin=False)
            atom['pdos'] = atm.pdos
        self.enary = self.atomlist[0]['pdos']['enary']

    def plotpdos(self, ax, orbital, geo='', ls='-', lw=1., ):
        '''
        orbital = 's' / 'p' / 'd'
        geo = 'description of system structure geometry'
        ls : linestyle
        lw : linewidth
        '''
        self.ax = ax
        colorlist = ('b', 'r', 'g', 'c', 'm', 'y')
        i = -1
        for atom in self.atomlist:
            i+=1
            color = colorlist[i%len(colorlist)]
            self.ax.plot(self.enary - self.fermi, atom['pdos'][orbital], color = color, label=geo+atom['elem']+' '+str(atom['atomid']), linestyle=ls, linewidth=lw )

