#! /usr/bin/env python3

import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from gaussian_fit import *

def del_nan(x, y):
    matxy = np.array((x,y)).transpose()
    matxy = matxy[~np.isnan(matxy).any(axis=1)]
    matxy = matxy.transpose()
    x = matxy[0]
    y = matxy[1]
    return x, y

# define Gaussian function initial guess

'''
     guess = [ 
               [amp_1, width_1, center_1],
               [amp_2, width_2, center_2],
               ...
               [offset]
             ]
'''

guess = [ 
          [10000., 30., 3200.], 
          [50000., 30., 3350.], 
          [10000., 30., 3500.], 
          [40.]
        ]

# load data
x, y, x1, y1 = np.genfromtxt('/home/jinxi/anyon_datastore/h2o_tms/au_h2o_sers.dat', delimiter=",", unpack=True, usecols=range(4)) 
# delete 'NaN' rows
x, y = del_nan(x, y)
# shift y with minimum
y -= min(y)

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


