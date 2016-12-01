
import numpy as np
from raman import cross_section

class Spectra:

    def __init__(self, freq, intens):
        self.freq = np.array(freq)
        self.intens = np.array(intens)

    def scaling(self, factor=1.0):
        self.freq = self.freq*factor

    def get_raman_section(self, freq_inc=632.8, temp=298.0,):
        '''
        Assume the input intensities ``self.intens`` are represented
        by Raman activity.
        '''
        self.raman_section = []
        for i, vibfreq in enumerate(self.freq):
            crsection = cross_section(vibfreq, self.intens[i], freq_inc, temp)
            self.raman_section.append(crsection)

    def broaden_lorentz(self, freq_ary, intens_list, fwhm=10., ):
        '''
        https://en.wikipedia.org/wiki/Cauchy_distribution
        '''
        gamma = 0.5*fwhm
        intens_ary = np.zeros(freq_ary.shape[0])
        for i, freq0 in enumerate(self.freq):
            intens_ary += intens_list[i]*(gamma/np.pi)/( (freq_ary-freq0)**2 + gamma**2 )
        self.freq_ary = freq_ary
        self.intens_ary = intens_ary
