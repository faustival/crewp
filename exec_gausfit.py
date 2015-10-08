#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
from peakvar import PeakVar

# define tag of all columns (e. g. potentials in EC-SERS)
inpfname = '/home/jinxi/anyon_datastore/h2o_tms/au_h2o_sers.csv'
taglist = [-2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8]
#taglist = [-2.0, -1.8, -1.6, -1.4, -1.2, -1.0]
taglist = [ '{:.1f}'.format(tag) for tag in taglist ]
plot_gfit_off_iter = 1000.

# define Gaussian function initial guess
'''
     guess = [ 
               [amp_1, width_1, center_1],
               [amp_2, width_2, center_2],
               ...
               [offset]
             ]
'''
gaus_guess_au =  { 
                "-2.0": [ 
                          [10000., 30., 3200.], 
                          [50000., 30., 3350.], 
                          [10000., 30., 3500.], 
                          [60.]
                        ], 
                "-1.6": [ 
                        [48046.61, 77.5, 3195.6], 
                        [237888.1, 99.7, 3357.4], 
                        [44327.58, 74.4, 3567.6], 
                        [52.5]
                        ], 
                "-1.2": [ 
                        [64800.6, 78.4, 3236.3], 
                        [146024.5, 74.6, 3382.4], 
                        [13584.7, 75.0, 3582.5], 
                        [61.22164]
                        ],
                "-0.8": [ 
                        [52178.74, 79.8, 3242.5], 
                        [167282.9, 80.5, 3419.5], 
                        [11572.01, 54.5, 3600.8], 
                        [52.3]
                        ],
                "-0.4": [ 
                        [5252.193, 37.32, 3172.0], 
                        [251493.0, 114.3, 3400.1], 
                        [34255.33, 73.68, 3664.2], 
                        [60.]
                        ],
              }

ecsers = PeakVar(inpfname, taglist)
# plot all loaded spectra to check the data
ecsers.plotall()
# fit Gaussian peaks and plot
ecsers.fitgauss(gaus_guess_au)
ecsers.plotgfit(plot_gfit_off_iter)
# linear regression of fitted frequencies and plot
ecsers.peak_linreg()
ecsers.plotfreqvar()

plt.show()


