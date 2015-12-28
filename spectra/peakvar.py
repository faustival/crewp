#! /usr/bin/env python3

import sys
import numpy as np
np.set_printoptions(threshold=np.nan)
from scipy.optimize import leastsq
from scipy import stats
import matplotlib.pyplot as plt
from spectra.spectrum import Spectrum

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

    def plotall(self):
        '''
        only plot experimental spectral lines
        to check the data loading
        '''
        self.fig_allspectra = plt.figure()
        ax_allspectra = self.fig_allspectra.add_subplot(1,1,1)
        for key in sorted(self.spectra.keys(), key=lambda val: float(val)):
            spectrum_data = self.spectra[key]
            ax_allspectra.plot(spectrum_data.x, spectrum_data.y, label=(key+' V'))
        ax_allspectra.legend()

    def fitgauss(self, gaus_guess):
        '''
        fit for each spectra 
        Gaussian fitted peak variation 
        OUTPUT
        ======
        self.keyvar = np.array( [ key1, key2, ... ] )
        self.freqvar = np.array( [ freq_array_of_1st_peak[ key1, key2, ... ] ]
                                 [ freq_array_of_2st_peak[ key1, key2, ... ] ] 
                                 ... )
        '''
        self.gfit_guess = gaus_guess
        self.keyvar = []
        self.freqvar = []
        for key in sorted(self.gfit_guess.keys(), key=lambda val: float(val)):
            spectrum = self.spectra[key]
            self.keyvar.append(float(key))
            spectrum.gausfit(self.gfit_guess[key])
            freqary = [ peak[0] for peak in spectrum.gfit_peak_pos ] 
            self.freqvar.append(freqary) 
            print(key, self.spectra[key].gfit_oup)
        self.keyvar = np.array(self.keyvar)
        self.freqvar = np.array(self.freqvar).transpose()

    def peak_linreg(self):
        '''
        linear regression results for peak variations:
        INPUT
        =====
        self.keyvar = np.array( [ key1, key2, ... ] )
        self.freqvar = np.array( [ freq_array_of_1st_peak[ key1, key2, ... ] ]
                                 [ freq_array_of_2st_peak[ key1, key2, ... ] ] 
                                 ... )
        OUTPUT
        ======
        self.linreg_oup = [ 
                            [ slope_1, intercept_1, r_value_1 ] 
                            [ slope_2, intercept_2, r_value_2 ] 
                            ...
                          ]
        self.linreg_line = [ slope_1 * self.keyvar + intercept_1 ,
                             slope_2 * self.keyvar + intercept_2 ,
                             ...
        '''
        self.linreg_oup = []
        self.linreg_line = []
        for i in range(0,self.freqvar.shape[0]):
            linreg_oup = stats.linregress(self.keyvar, self.freqvar[i])
            slope, intercept, r_value, p_value, std_err = linreg_oup
            self.linreg_oup.append([slope, intercept, r_value])
            self.linreg_line.append( slope * self.keyvar + intercept )
        print(self.linreg_oup)

    def plotgfit(self, ax_gfit, off_iter, pltguess=True):
        '''
        ax_gfit  : axis container assigned to plot in
        off_iter : offset between each variation of spectrum (spectroscopic sample condition)
        pltguess : if True, plot the initial guessed line
        '''
        off = -off_iter
        for key in sorted( self.gfit_guess.keys(), key=lambda val: float(val) ):
            off += off_iter
            self.spectra[key].offsetall(off)
            self.spectra[key].plot_gfit(ax_gfit, pltguess)
            ax_gfit.text( min(self.spectra[key].x)-60., min(self.spectra[key].y), '%.2f V' % (float(key)) , 
                        horizontalalignment='center',
                        verticalalignment='bottom')
            self.spectra[key].offsetall(-off)

    def plotfreqvar(self, ax_freqvar):
        colorlist = ('g', 'c', 'm', 'y')
        counter = -1
        for i in range(0,self.freqvar.shape[0]):
            counter += 1
            color = colorlist[counter % len(colorlist)]
            ax_freqvar.plot(self.keyvar, self.freqvar[i], 'ro', color=color)
            ax_freqvar.plot(self.keyvar, self.linreg_line[i], color=color)





