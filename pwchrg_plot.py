#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from pwchrg import read_pwchrg


inpfname = 'ag100chrg.log'
chrg = read_pwchrg(inpfname)
avgchrg = [np.mean(chrg[i,:,:]) for i in range(320)]
avgchrg = np.array(avgchrg)
print(chrg[1,:,:].shape)
print(avgchrg.shape)

fig = plt.figure()
plt.plot
ax = fig.add_subplot( 1, 1, 1)
#ax.plot(chrg[:,15,15])
ax.plot(avgchrg)

plt.show()

