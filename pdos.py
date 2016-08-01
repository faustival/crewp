#! /usr/bin/python3

import numpy as np
from .qe.atom import Atom

class PDOS:
    '''
    processing PDOS in a single computation, i.e. system sharing same:
    * fermi energy should be naturally the same.
    * energy array

    Two functions:
    * load all PDOS in atomdict, and updated as self.atomdict[i]['pdos']
    * plot pdos
    '''

    def __init__(self, atomdict, fermi, readtot=False):
        '''
        atomdict = {
                    '13':{ 'elem':'Pd', 'orbitals':{'d':['tot','x2-y2'],},
                    '14':{ 'elem':'Pd', 'orbitals':{'d':['tot','zx'],},},
                   {
        preserve for ``atomdict`` after pdos reading, 
        to keep a sequencial record of angular-orbitals
        '''
        self.atomdict = atomdict
        self.fermi = fermi
        self.getpdos()
        if readtot:
            cols = np.loadtxt('plt.pdos_tot', unpack=True)
            self.totread = cols[2]

    def getpdos(self):
        '''
        self.atomdict['id']['pdos'] was updated.
        '''
        for atomid, atom in self.atomdict.items():
            atomobj = Atom(atomid, atom['elem'])
            atomobj.get_pdos('plt', atom['orbitals'], spin=False)
            atom['pdos'] = atomobj.pdos
            if not hasattr(self, 'enary'):
                self.enary = atomobj.pdos_enary

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
        pdos_sum = np.zeros((enary.shape[0]))
        for atomid, orbitaldict in aodict.items():
            for orbital, angularlist in orbitaldict.items():
                for angular in angularlist:
                    pdos_sum += self.atomdict[atomid]['pdos'][orbital][angular]
        return enary, pdos_sum
    
    def sumpdos_all(self):
        '''
        sum all pdos contribution from ``self.atomdict``
        Be careful if [orbital]['tot'] is included
        '''
        aolist = [ i for i in self.atomdict.keys() ]
        aodict = self.get_sum_aodict(aolist)
        enary, pdos_sum = self.sumpdos(aodict)
        return enary, pdos_sum

    def plotpdos(self, ax, orbital, angular, plot_pref='', ls='-', lw=1., ):
        '''
        orbital = 's' / 'p' / 'd'
        geo = 'description of system structure geometry'
        ls : linestyle
        lw : linewidth
        '''
        self.ax = ax
        colorlist = ('b', 'r', 'g', 'c', 'm', 'y')
        i = -1
        for atomid in sorted(list(self.atomdict.keys())):
        #for atomid, atom in self.atomdict.items():
            atom = self.atomdict[atomid]
            i+=1
            color = colorlist[i%len(colorlist)]
            line, = self.ax.plot(self.enary - self.fermi, atom['pdos'][orbital][angular], color = color, label=plot_pref+atom['elem']+' '+atomid, linestyle=ls, linewidth=lw )
            if ls=='--':
                line.set_dashes([5,2.5])



