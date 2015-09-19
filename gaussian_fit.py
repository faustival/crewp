#! /usr/bin/env python3

import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def del_nan(x, y):
    matxy = np.array((x,y)).transpose()
    matxy = matxy[~np.isnan(matxy).any(axis=1)]
    matxy = matxy.transpose()
    x = matxy[0]
    y = matxy[1]
    return x, y

def gaussian(x, amp, width, center, offset):
    gaussian = amp / np.sqrt(2.*np.pi*width**2) * np.exp( -(x-center)**2/(2.*width**2) ) + offset
    return gaussian

def gaussian0(x, amp, width, center):
    gaussian = amp / np.sqrt(2.*np.pi*width**2) * np.exp( -(x-center)**2/(2.*width**2) ) 
    return gaussian

def sumgaus(par, x):
    sumgaus = np.zeros(x.size)
    for i in range(0,len(par)//4):
        arg_gaus = par[4*i:4*(i+1)]
        amp, width, center, offset = arg_gaus
        sumgaus += gaussian(x, amp, width, center, offset)
    return sumgaus

def sumgaus0(par, x):
    sumgaus = np.zeros(x.size)
    for i in range(0,len(par)//3):
        arg_gaus = par[3*i:3*(i+1)]
        amp, width, center = arg_gaus
        sumgaus += gaussian0(x, amp, width, center)
    offset = par[-1]
    sumgaus += offset
    return sumgaus

def residues(par, y, x):
    print(par)
    gaussum = sumgaus0(par, x)
    err = y - gaussum
    return err

def reorgpar(inp):
    oup=[]
    for item in inp:
        oup += item
    return oup

# define Gaussian function initial guess
'''
        [amp, width, center, offset] = arg_gaus
'''
guess = [ 
         [50000., 30., 3300., 40.], 
         [10000., 30., 3500., 0.], 
        ]

guess0 = [ 
         [50000., 30., 3300.], 
         [10000., 30., 3500.], 
         [40.]
        ]

# load data
x, y, x1, y1 = np.genfromtxt('/home/jinxi/au_h2o_sers.dat', delimiter=",", unpack=True, usecols=range(4)) 
# delete 'NaN' rows
x, y = del_nan(x, y)
# shift y with minimum
y -= min(y)

par0 = reorgpar(guess0)

parout = leastsq(residues, par0, args=(y, x))

print(par0)
print(parout)

plt.plot(x, y,  label='Experiment', color='blue')
#plt.plot(x, sumgaus0(par0,x),  label='Initial')
plt.plot(x, sumgaus0(parout[0],x),  label='Optimized', color='red', linewidth=2.)
parplot = parout[0]
colorlist = ('g', 'c', 'm', 'y')
counter = -1
for i in range(0,len(parplot)//3):
    counter += 1
    color = colorlist[counter % len(colorlist)]
    arg_gaus = parplot[3*i:3*(i+1)]
    amp, width, center = arg_gaus
    plotiso = gaussian0(x, amp, width, center) + parplot[-1]
    plt.plot(x, plotiso,  label='Optimized peak %d'%i, color=color, linestyle='--', dashes=(5,1.5), linewidth=1.5)
plt.legend()
plt.show()


