#! /usr/bin/python3

import numpy as np

a = np.arange(1,7)
print(a)

c = np.reshape(a,(2,3))
print('(2,3) ',c)

f = np.reshape(a,(3,2),order='C')
print('(3,2) ',f)
