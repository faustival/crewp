#! /usr/bin/python3

import sys
from crewp.gaussian.oupf import Oupf

fname = sys.argv[1]

print('Reading Gaussian output, ', fname)

freqf = Oupf(fname)
freqf.get_vib_auto()

for i, seq in enumerate(freqf.vib_modeseq):
    print('{:5d}, {:13.5f} {:13.5f} {:13.5f} '.format(seq, freqf.vib_freq[i], freqf.ir_intens[i], freqf.raman_activ[i]))
