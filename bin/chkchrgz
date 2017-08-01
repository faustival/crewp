#! /usr/bin/env python3

import sys
import os
import numpy as np

import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt

from crewp.middleware.chrgden import get_chrg_avgz

# read in CHGCAR filename series from command-line
packname = sys.argv[1]
chrgf_list = sys.argv[2:]

print( sys.version )
print( 'Readin: ', chrgf_list )

for fname in chrgf_list:
    total_valence = get_chrg_avgz(fname, packname, callmethod='chkchrg')
    print( '    '+fname, ' total valence charge: ', total_valence)

