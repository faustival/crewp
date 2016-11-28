#! /usr/bin/python3

import sys
from crewp.gaussian.oupf import Oupf

fname = sys.argv[1]

print('Reading Gaussian output, ', fname)

oupf_obj = Oupf(fname)

