#! /usr/bin/env python3

import sys
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

'''
functions fitting overlapping experimental peaks to isolated Gaussians
reorgpar, gaussian, sumgaus, residues

See the example of least-square fitting,
http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html

Define the initial guess of gaussian function parameters as:

     guess = [ 
               [amp_1, width_1, center_1],
               [amp_2, width_2, center_2],
               ...
               [offset]
             ]
'''

def reorgpar(inp):
    oup=[]
    for item in inp:
        oup += item
    return oup

def gaussian(x, amp, width, center):
    gaussian = amp / np.sqrt(2.*np.pi*width**2) * np.exp( -(x-center)**2/(2.*width**2) ) 
    return gaussian

def sumgaus(par, x):
    sumgaus = np.zeros(x.size)
    for i in range(0,len(par)//3):
        arg_gaus = par[3*i:3*(i+1)]
        amp, width, center = arg_gaus
        sumgaus += gaussian(x, amp, width, center)
    offset = par[-1]
    sumgaus += offset
    return sumgaus

def residues(par, y, x):
    #print(par)
    gaussum = sumgaus(par, x)
    err = y - gaussum
    return err

class Spectrum:
    '''
    Spectrum line analysis
    '''
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def gausfit(self, guess):
        '''
        fit Gaussian functions
        '''
        self.gfit_guess = guess
        par0 = reorgpar(self.gfit_guess)
        fitoup = leastsq(residues, par0, args=(self.y, self.x))
        parout = fitoup[0]
        # reform the fitting output parameters like the input
        self.gfit_oup = []
        for i in range(0,len(parout)//3):
            self.gfit_oup.append( list( parout[3*i:3*(i+1)] ) )
        self.gfit_oup.append( [ parout[-1] ] )

    def plotfit(self):
        self.fig_gausfit = plt.figure()
        ax_gfit = self.fig_gausfit.add_subplot(1,1,1)
        ax_gfit.plot(self.x, self.y,  label='Experiment', color='blue')
        ax_gfit.plot(self.x, sumgaus( reorgpar(self.gfit_guess), self.x ),  label='Initial')
        ax_gfit.plot(self.x, sumgaus( reorgpar(self.gfit_oup), self.x ),  label='Optimized', color='red', linewidth=2.)
        colorlist = ('g', 'c', 'm', 'y')
        counter = -1
        for i in range(0,len(self.gfit_oup)-1):
            counter += 1
            color = colorlist[counter % len(colorlist)]
            amp, width, center = self.gfit_oup[i]
            [offset] = self.gfit_oup[-1]
            plotiso = gaussian(self.x, amp, width, center) + offset
            ax_gfit.plot(self.x, plotiso,  label='Optimized peak %d'%i, color=color, linestyle='--', dashes=(5,1.5), linewidth=1.5)
        ax_gfit.legend()





