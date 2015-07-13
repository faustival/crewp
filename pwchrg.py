#! /usr/bin/python3

import numpy as np
from scipy.integrate import simps

class PWCharge:
    '''
    By default use atomic (Bohr) unit.
    '''

    def __init__(self, chrg, cell, unit='bohr'):
        bohr2ang = 0.529177
        if unit=='ang':
            chrg = chrg/bohr2ang**3
            cell = cell*bohr2ang
        self.chrg = chrg
        self.cell = cell
        self.ngridz = self.chrg.shape[0]

    def xyavg(self):
        avgchrg = [np.mean(self.chrg[i,:,:]) for i in range(self.ngridz)]
        avgchrg = np.array(avgchrg)
        return avgchrg

    def zgrid(self):
        zaxis = np.linspace(0., self.cell[2,2], self.ngridz)
        return zaxis

    def xyarea(self):
        xycross = np.cross(self.cell[0], self.cell[1])
        xyarea = np.linalg.norm(xycross)
        return xyarea

    def intgrl_z(self):
        '''
        mainly for check the average
        '''
        xyarea = self.xyarea()
        avgchrg = self.xyavg()
        zaxis = self.zgrid()
        total_valence = xyarea*simps(avgchrg, zaxis)
        return total_valence



