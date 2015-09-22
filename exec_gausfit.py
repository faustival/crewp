#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
from peakvar import PeakVar

# define tag of all columns (e. g. potentials in EC-SERS)

inpfname = '/home/jinxi/anyon_datastore/h2o_tms/au_h2o_sers.dat'
taglist = [-2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8]
taglist = [ '{:.1f}'.format(tag) for tag in taglist ]

sers = PeakVar(inpfname, taglist)

sys.exit()

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
                          [40.]
                        ], 

                "-1.6": [ 
                          [10000., 30., 3200.], 
                          [50000., 30., 3350.], 
                          [10000., 30., 3500.], 
                          [40.]
                        ], 
              }

par0 = reorgpar(guess)

parout = leastsq(residues, par0, args=(y, x))

print(par0)
print(parout)

plt.plot(x, y,  label='Experiment', color='blue')
plt.plot(x, sumgaus(par0,x),  label='Initial')
plt.plot(x, sumgaus(parout[0],x),  label='Optimized', color='red', linewidth=2.)
parplot = parout[0]
colorlist = ('g', 'c', 'm', 'y')
counter = -1
for i in range(0,len(parplot)//3):
    counter += 1
    color = colorlist[counter % len(colorlist)]
    arg_gaus = parplot[3*i:3*(i+1)]
    amp, width, center = arg_gaus
    plotiso = gaussian(x, amp, width, center) + parplot[-1]
    plt.plot(x, plotiso,  label='Optimized peak %d'%i, color=color, linestyle='--', dashes=(5,1.5), linewidth=1.5)
plt.legend()
plt.show()


