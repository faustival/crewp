#! /usr/bin/python3

import numpy as np

'''
basic quantities for condensed matter
'''

bohr2ang = 0.529177

# electron density
a_ang = 4.08 #ang
e_per_cube = 4.
a_au = a_ang/bohr2ang
rho = e_per_cube/a_au**3

# rs in Bohr
rs = (3./(4.*np.pi*rho))**(1/3)

print('rho = ', rho)
print('rs = ', rs)
