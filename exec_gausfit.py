#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
from peakvar import PeakVar
from spectrum import *

# define tag of all columns (e. g. potentials in EC-SERS)
inpfname = '/home/jinxi/anyon_datastore/h2o_tms/au_h2o_sers.dat'
taglist = [-2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8]
taglist = [ '{:.1f}'.format(tag) for tag in taglist ]

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
#                          [10000., 30., 3200.], 
                          [50000., 30., 3350.], 
                          [10000., 30., 3500.], 
                          [40.]
                        ], 

                "-1.6": [ 
#                          [10000., 30., 3200.], 
                          [100000., 50., 3300.], 
                          [10000., 30., 3500.], 
                          [40.]
                        ], 
              }

sers = PeakVar(inpfname, taglist)
sers.fitgauss(gaus_guess)
sers.spectra["-2.0"].plotfit()
sers.spectra["-1.6"].plotfit()

plt.show()


