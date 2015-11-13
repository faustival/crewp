#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from spectrum import Spectrum

inpfname = '/home/jinxi/anyon_datastore/h2o_tms/pinge.csv'
cols = np.genfromtxt(inpfname, delimiter=",", unpack=True) 

guess = [ 
       [200., 20., 600.],
       [9144.6528, 28.5630, 687.3294],
       [7.0]
     ]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

spectrum = Spectrum(cols[0],cols[1])
spectrum.gausfit(guess)
print(spectrum.gfit_oup)

ax.plot(spectrum.x, spectrum.y)
spectrum.plot_gfit(ax)

plt.show()


