#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
from peakvar import PeakVar
from ecsers_gfit_guesses import *

inpfname = '/home/jinxi/anyon_datastore/h2o_tms/pt_h2o_sers.csv'
# define tag of all columns (e. g. potentials in EC-SERS)
#taglist = [-2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8]
taglist = [-2.0, -1.8, -1.6, -1.4, -1.2, -1.0]
gfit_guess = gfit_guess_pt_3p
plot_gfit_off_iter = 1000.
plt_gfit_guess = False


taglist = [ '{:.1f}'.format(tag) for tag in taglist ]
ecsers = PeakVar(inpfname, taglist)
# plot all loaded spectra to check the data
ecsers.plotall()
# fit Gaussian peaks
ecsers.fitgauss(gfit_guess)
# linear regression of fitted frequencies 
ecsers.peak_linreg()

# plot gaussian fit result
fig_gausfit = plt.figure()
ax_gfit = fig_gausfit.add_subplot(1,1,1)
ecsers.plotgfit(ax_gfit, plot_gfit_off_iter, plt_gfit_guess)
# plot linear regression result
fig_freqvar = plt.figure()
ax_freqvar = fig_freqvar.add_subplot(1,1,1)
ecsers.plotfreqvar(ax_freqvar)

plt.show()


