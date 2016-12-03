#! /usr/bin/python3

import sys
import numpy as np
from crewp.gaussian.oupf import Oupf
from crewp.spectra.spectra import Spectra
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt

'''
# setup parameters
'''
try:
    scale_factor = float(sys.argv[1])
    fname = sys.argv[2]
except ValueError:
    scale_factor = 1.0
    fname = sys.argv[1]

'''
# Reading from Gaussian output
'''
print('Reading Gaussian output, ', fname)
freqf = Oupf(fname)
freqf.get_vib_auto()
for i, seq in enumerate(freqf.vib_modeseq):
    print('{:5d}, {:13.5f} {:13.5f} {:13.5f} '.format(seq, freqf.vib_freq[i], freqf.ir_intens[i], freqf.raman_activ[i]))

spectra = Spectra(freqf.vib_freq, freqf.raman_activ)

# Scaling 
spectra.scaling(scale_factor)

# calculate cross section
spectra.get_raman_section(632.8, 298.0)

# Broadening
freq_ary = np.arange(0., 3500., 0.5)
spectra.broaden_lorentz(freq_ary, spectra.raman_section, 10.)

# Write data
spectra.wrt_csv( '(cm-1)', '(m^2/sr)' )

# Plot
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#ax.stem(spectra.freq, spectra.raman_section)
ax.plot(spectra.freq_ary, spectra.intens_ary)
plt.show()



