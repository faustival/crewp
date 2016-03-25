#! /usr/bin/python3

import numpy as np
from qescripts.atom import Atom

class PDOS:
    '''
    processing PDOS in a single computation, i.e. system sharing same:
    * fermi energy should be naturally the same.
    * energy array

    Two functions:
    * load all PDOS in atomdict, and updated as self.atomdict[i]['pdos']
    * plot pdos
    '''

    def __init__(self, atomdict, fermi):
        '''
        atomdict = {
                    '13':{ 'elem':'Pd', 'orbitals':{'d':['tot','x2-y2'],},
                    '14':{ 'elem':'Pd', 'orbitals':{'d':['tot','zx'],},},
                   {
        '''
        self.atomdict = atomdict
        self.fermi = fermi
        self.getpdos()

    def getpdos(self):
        '''
        self.atomdict['id']['pdos'] was updated.
        '''
        for atomid, atom in self.atomdict.items():
            atomobj = Atom(atomid, atom['elem'])
            atomobj.get_pdos('plt', atom['orbitals'], spin=False)
            atom['pdos'] = atomobj.pdos
        self.enary = list(self.atomdict.values())[0]['pdos']['enary']

    def get_sum_aodict(self, aolist):
        '''
        Build atomic orbital dictionary, prepare for sumpdos method,
        from atom ID list as integer
        aolist = [13, 14]
        useful when summation of PDOS orbital-angular dictionary is the same as reading
        '''
        aodict = {}
        for i in aolist:
            atomid = str(i)
            aodict[atomid] = self.atomdict[atomid]['orbitals']
        return aodict

    def sumpdos(self, aodict):
        '''
        Sum PDOS with a dictionary definition.
        Useful when testing MO assignment from atomic orbital combinations.
        aodict = { 
                  '13' : { 
                           's' : ['tot'],
                         },
                  '14' : { 
                           'p' : ['z'],
                           'd' : ['z2', 'xy'],
                         },
                 }
        '''
        enary = self.enary
        sumpdos = np.zeros((enary.shape[0]))
        for atomid, orbitaldict in aodict.items():
            for orbital, angularlist in orbitaldict.items():
                for angular in angularlist:
                    sumpdos += self.atomdict[atomid]['pdos'][orbital][angular]
        return enary, sumpdos

    def plotpdos(self, ax, orbital, angular, geo='', ls='-', lw=1., ):
        '''
        orbital = 's' / 'p' / 'd'
        geo = 'description of system structure geometry'
        ls : linestyle
        lw : linewidth
        '''
        self.ax = ax
        colorlist = ('b', 'r', 'g', 'c', 'm', 'y')
        i = -1
        for atomid, atom in self.atomdict.items():
            i+=1
            color = colorlist[i%len(colorlist)]
            self.ax.plot(self.enary - self.fermi, atom['pdos'][orbital][angular], color = color, label=geo+atom['elem']+' '+atomid, linestyle=ls, linewidth=lw )

