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
gfit_guess = gfit_guess_pt
plot_gfit_off_iter = 1000.


taglist = [ '{:.1f}'.format(tag) for tag in taglist ]
ecsers = PeakVar(inpfname, taglist)
# plot all loaded spectra to check the data
ecsers.plotall()
# fit Gaussian peaks and plot
ecsers.fitgauss(gfit_guess)
ecsers.plotgfit(plot_gfit_off_iter)
# linear regression of fitted frequencies and plot
ecsers.peak_linreg()
ecsers.plotfreqvar()

plt.show()


