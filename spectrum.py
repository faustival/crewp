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

Call the fitting as, 

    par0 = reorgpar(guess)
    fitoup = leastsq(residues, par0, args=(spectrum.y, spectrum.x))
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
        Output:
        =======
        self.y_gfit_guess : peak computed with initial guess parameters
        self.y            : shifted to fitted baseline
        self.y_gfit_sum   : fitted peak sum, shifted baseline to 0
        self.y_gfit_peaks : fitted peaks list, shifted baseline to 0
        '''
        self.gfit_guess = guess
        self.y -= min(self.y)
        par0 = reorgpar(self.gfit_guess)
        fitoup = leastsq(residues, par0, args=(self.y, self.x))
        parout = fitoup[0]
        # reform the fitting output parameters like the input
        self.gfit_oup = []
        for i in range(0,len(parout)//3):
            self.gfit_oup.append( list( parout[3*i:3*(i+1)] ) )
        self.gfit_oup.append( [ parout[-1] ] )
        # compute for the estimated and fitted spectra
        self.y_gfit_sum = sumgaus( reorgpar(self.gfit_oup), self.x )
        self.y_gfit_peaks = []
        for i in range(0,len(self.gfit_oup)-1):
            amp, width, center = self.gfit_oup[i]
            [offset] = self.gfit_oup[-1]
            peak = gaussian(self.x, amp, width, center) + offset
            self.y_gfit_peaks.append(peak)
        self.y_gfit_guess = sumgaus( reorgpar(self.gfit_guess), self.x )
        # shift fitted baseline to 0
        [off] = self.gfit_oup[-1]
        self.offsetall(-off)

    def offsetall(self, offset):
        '''
        shift off spectrum 
        '''
        self.y_gfit_guess += offset
        self.y += offset
        self.y_gfit_sum += offset
        for peak in self.y_gfit_peaks:
            peak += offset

    def plot_gfit(self, ax_gfit):
        ax_gfit.plot(self.x, self.y,  label='Experiment', color='blue')
        #ax_gfit.plot(self.x, self.y_gfit_guess, label='Initial', color='black')
        ax_gfit.plot(self.x, self.y_gfit_sum, label='Optimized', color='red', linewidth=2.)
        colorlist = ('g', 'c', 'm', 'y')
        counter = -1
        for peak in self.y_gfit_peaks:
            counter += 1
            color = colorlist[counter % len(colorlist)]
            ax_gfit.plot(self.x, peak, label='Optimized peak %d'%(counter+1), color=color, linestyle='--', dashes=(5,1.5), linewidth=1.5)
        ax_gfit.legend()





