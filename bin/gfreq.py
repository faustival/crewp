#! /usr/bin/env python3

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
    fname_list = sys.argv[2:]
except ValueError:
    scale_factor = 1.0
    fname_list = sys.argv[1:]

'''
# initialize figure 
'''
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

for i, fname in enumerate(fname_list):
    '''
    # Reading from Gaussian output
    '''
    print('Reading Gaussian output, ', fname)
    freqf = Oupf(fname)
    freqf.get_vib_auto()
    # print unscaled freq list
    #for i, seq in enumerate(freqf.vib_modeseq):
    #    print('{:5d}, {:13.5f} {:13.5f} {:13.5f} '.format(seq, freqf.vib_freq[i], freqf.ir_intens[i], freqf.raman_activ[i]))
    spectra = Spectra(freqf.vib_freq, freqf.raman_activ)
    spectra.scaling(scale_factor)
    spectra.get_raman_section(632.8, 298.0)
    freq_ary = np.arange(0., 3500., 0.5)
    spectra.broaden_lorentz(freq_ary, spectra.raman_section, 10.)
    spectra.wrt_csv( '(cm-1)', '(m^2/sr)', datfname='spectra_'+str(i)+'.dat' )
    #ax.stem(spectra.freq, spectra.raman_section)
    ax.plot(spectra.freq_ary, spectra.intens_ary, label=fname)
ax.legend(loc=2)
plt.show()



