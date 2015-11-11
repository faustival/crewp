#! /usr/bin/python3

import numpy as np
import sys

class Atom:

    def __init__(self, atomid, elem):
        '''
        self.atomid : atom ID in output, integer
        self.elem : element of atom, string
        '''
        self.atomid = atomid
        self.elem = elem

    def get_ldos(self, oupfpre, orbitals, readpdos=True, spin=True):
        '''
        Read the pdos files of the atom.

        pdos file structure:
        ====================
        <beginning of file>
        # E (eV)  ldosup(E)  ldosdw(E) pdosup(E)  pdosdw(E)  ...
         -6.759  0.944E-07  0.942E-07  0.944E-07  0.942E-07  ...
         ...
         ...
        <end of file>

        pdos : projected on each atomic orbitals, e.g., p_x, p_y, p_z
        ldos : sum of pdos

        INPUT:
        ======
        oupfpre : prefix of pdos files, indicated by QE input ``filpdos`` of projwfc.x 
        readpdos : if True, read pdos and ldos
                   if False, read only ldos
        orbitals : list of projection orbitals, ['s','p',...]

        NEW Attributes:
        ===============
        self.ldos = { 'enary': np.array[energy array], 
                      's': np.array[s array], 
                      'p': np.array[p array],
                      ... }
        '''
        # dictionary building correspondence of orbital ID
        orbital_dict = { 's':'1', 'p':'2', 'd':'3', 'f':'4' }
        self.ldos = {}
        for orbital in orbitals:
            pdosfname = oupfpre + \
                        '.pdos_atm#' + str(self.atomid) + \
                        '(' + self.elem + ')_wfc#' + \
                        orbital_dict[orbital] + '(' + orbital + ')'
            print('Reading', pdosfname, '...')
            cols = np.loadtxt(pdosfname, unpack=True)
            if 'enary' not in self.ldos:
                self.ldos['enary'] = cols[0]
            if not spin:
                self.ldos[orbital] = cols[1]
            elif spin:
                self.ldos[orbital] = cols[1:3]
            if readpdos:
                print('PDOS reading not implemented yet!')
                sys.exit()

                      





