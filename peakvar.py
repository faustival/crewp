#! /usr/bin/env python3

import sys
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from spectrum import Spectrum

class PeakVar:
    '''
    Peak variations manipulation:
    * Load data
    * Gaussian fit
    * Interpolation
    '''

    def __init__(self, inpfname, taglist):
        self.inpfname = inpfname
        self.taglist = taglist
        self.spectra = {}
        self.loaddata()

    def loaddata(self):
        '''
        Load all data from file:
        * prepared as CSV format
        * comment the tag row with '#'

        build the db with:
        self.spectra = { 
                         taglist[0] : Spectrum instance for taglist[0],
                         taglist[1] : Spectrum instance for taglist[1],
                         ...
                       }

        '''
        cols = np.genfromtxt(self.inpfname, delimiter=",", unpack=True) 
        if cols.shape[0] != 2*len(self.taglist):
            print("ERROR! mismatch of taglist and column!")
            sys.exit()
        for i in range(len(self.taglist)):
            colxy = cols[2*i:2*i+2]
            # delete rows containing 'NaN'
            colxy = colxy.transpose()
            colxy = colxy[~np.isnan(colxy).any(axis=1)]
            colxy = colxy.transpose()
            # add i-th spectra instance to self.spectra{}
            self.spectra[self.taglist[i]] = Spectrum(colxy[0], colxy[1])

    def fitgauss(self, gaus_guess):
        '''
        fit for each spectra 
        '''
        self.gfit_guess = gaus_guess
        self.voltvar = []
        self.peakvar = []
        for key in sorted(self.gfit_guess.keys()):
            spectrum = self.spectra[key]
            self.voltvar.append(float(key))
            spectrum.gausfit(self.gfit_guess[key])
            freqary = [ peak[0] for peak in spectrum.gfit_peak_pos ] 
            self.peakvar.append(freqary) 
            print(key, self.spectra[key].gfit_oup)
        self.voltvar = np.array(self.voltvar)
        self.peakvar = np.array(self.peakvar).transpose()

    def plotgfit(self, off_iter):
        self.fig_gausfit = plt.figure()
        ax_gfit = self.fig_gausfit.add_subplot(1,1,1)
        off = -off_iter
        for key in sorted(self.gfit_guess.keys()):
            off += off_iter
            self.spectra[key].offsetall(off)
            self.spectra[key].plot_gfit(ax_gfit)
            ax_gfit.text( min(self.spectra[key].x)-60., min(self.spectra[key].y), '%.2f V' % (float(key)) , 
                        horizontalalignment='center',
                        verticalalignment='bottom')
            self.spectra[key].offsetall(-off)

    def plotfreqvar(self):
        self.fig_freqvar = plt.figure()
        ax_freqvar = self.fig_freqvar.add_subplot(1,1,1)
        for i in range(0,self.peakvar.shape[0]):
            ax_freqvar.plot(self.voltvar, self.peakvar[i])#,  label='Experiment', color='blue')

    def freqvar(self):
        '''
        Linear regression of Stark slope from Gaussian fitted 
        spectroscopy
        '''
        pass
        #for key in sorted(self.gfit_guess.keys()):




