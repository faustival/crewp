
import numpy as np
from crewp.cuconv.constants import epsilon0,planck,boltzmann,clight
from crewp.cuconv.uconv import ang2meter

def cross_section(vibfreq, activity, freq_inc=632.8, temp=298.0,):
    '''
    Reference paper:
    J. Neugebauer, M. Reiher, C. Kind, B. A. Hess, J. Comp. Chem., 23, 895, (2002).
    =====
    INPUT
    =====
    vibfreq    : vibrational frequency, in wavenumber, cm-1
    activity: Raman activity, unit Ang^4/amu
              Temporarily follow the double-harmonic approx.,
              that only first derivatives of polarizability contributes.
    freq_inc: frequency of incident laser. in wavelength, nm
    ======
    OUTPUT
    ======
    crsection: Raman differential scattering cross section, m^2/sr
    '''
    '''
    # Unit conversion to SI
    '''
    # Raman activity, S
    s = activity*(ang2meter**4)*(4*np.pi*epsilon0)**2 
    # Vibrational frequency, wavenumber, \nu cm-1 to m-1
    wvn = 100.*vibfreq
    laser = 1/freq_inc*1.e9
    '''
    # Calculate in parts
    '''
    boltzcorr = 1./( 1. - np.exp( -planck*clight*wvn/(boltzmann*temp) ) )
    prefactor = ( (laser-wvn)**4/wvn )*planck/(45.*8.*clight*epsilon0**2)
    crsection = prefactor*boltzmann*s
    return crsection



