#! /usr/bin/python3

import numpy as np
from scipy.integrate import simps

class SlabIndChrg:
    '''
    All z-dependent array must in the same z-grid
    '''

    def __init__(self, chrgf, chrg0, zaxis):
        self.zaxis = zaxis
        self.chrgf = chrgf
        self.chrg0 = chrg0
        self.chrgind = self.chrgf - self.chrg0

    def imgplane(self, slabcenter):
        # extract proper integrate region
        idx_center = np.argmin(np.absolute(self.zaxis-slabcenter))
        chrgind_var = self.chrgind[idx_center:]
        zaxis_var = self.zaxis[idx_center:]
        # calculate the image plane position
        int_zrho = simps(chrgind_var*zaxis_var, zaxis_var)
        int_rho = simps(chrgind_var, zaxis_var)
        self.z0 = int_zrho/int_rho
        return self.z0
