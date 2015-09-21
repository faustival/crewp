#! /usr/bin/env python3

import numpy as np
from scipy.optimize import leastsq

'''
functions fitting overlapping experimental peaks to isolated Gaussians

See the example of least-square fitting,
http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html

Define the initial guess of gaussian function parameters as:

     guess = [ 
               [amp_1, width_1, center_1],
               [amp_2, width_2, center_2],
               ...
               [offset]
             ]
'''

def reorgpar(inp):
    oup=[]
    for item in inp:
        oup += item
    return oup

def gaussian(x, amp, width, center):
    gaussian = amp / np.sqrt(2.*np.pi*width**2) * np.exp( -(x-center)**2/(2.*width**2) ) 
    return gaussian

def sumgaus(par, x):
    sumgaus = np.zeros(x.size)
    for i in range(0,len(par)//3):
        arg_gaus = par[3*i:3*(i+1)]
        amp, width, center = arg_gaus
        sumgaus += gaussian(x, amp, width, center)
    offset = par[-1]
    sumgaus += offset
    return sumgaus

def residues(par, y, x):
    #print(par)
    gaussum = sumgaus(par, x)
    err = y - gaussum
    return err



