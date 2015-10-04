#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
from peakvar import PeakVar

# define tag of all columns (e. g. potentials in EC-SERS)
inpfname = '/home/jinxi/anyon_datastore/h2o_tms/au_h2o_sers.dat'
taglist = [-2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8]
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
gaus_guess =  { 
                "-2.0": [ 
                          [10000., 30., 3200.], 
                          [50000., 30., 3350.], 
                          [10000., 30., 3500.], 
                          [60.]
                        ], 

                "-1.6": [ 
                        [5252.193, 37.32, 3172.0], 
                        [251493.0, 114.3, 3330.1], 
                        [34255.33, 73.68, 3564.2], 
                        [60.]
                        ], 
                "-1.2": [ 
                        [5252.193, 37.32, 3172.0], 
                        [251493.0, 114.3, 3330.1], 
                        [34255.33, 73.68, 3564.2], 
                        [60.]
                        ],
                "-0.8": [ 
                        [5252.193, 37.32, 3172.0], 
                        [251493.0, 114.3, 3400.1], 
                        [34255.33, 73.68, 3564.2], 
                        [60.]
                        ],
                "-0.4": [ 
                        [5252.193, 37.32, 3172.0], 
                        [251493.0, 114.3, 3400.1], 
                        [34255.33, 73.68, 3664.2], 
                        [60.]
                        ],
              }

ecsers = PeakVar(inpfname, taglist)
ecsers.fitgauss(gaus_guess)
ecsers.plotgfit(plot_gfit_off_iter)
ecsers.plotfreqvar()

plt.show()


