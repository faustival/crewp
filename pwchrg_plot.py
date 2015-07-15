#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from pwchrg_read import pwchrg_read
from pwchrg import PWCharge

inpfname = 'ag100f000_5layer/ag100chrg_d.log'

chrg, cell = pwchrg_read(inpfname)

slabchrg = PWCharge(chrg, cell, 'ang')

print('charge ang, ',slabchrg.intgrl_z())

avgchrg = slabchrg.xyavg()
zaxis = slabchrg.zgrid()

fig = plt.figure()
plt.plot
ax = fig.add_subplot( 1, 1, 1)
ax.plot(zaxis,avgchrg)
plt.show()


