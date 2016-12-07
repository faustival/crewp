
import numpy as np
from crewp.cuconv.constants_gaussian import planck,boltzmann,clight
from crewp.cuconv.uconv import ang2cm,amu2g

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
    crsection: Raman differential scattering cross section, cm^2/sr
    '''
    # Raman activity, S, Unit conversion to CGS-Gaussian 
    s = activity*(ang2cm**4/amu2g)**2
    laserfreq = 1./freq_inc*1.e7
    '''
    # Calculate in parts
    '''
    boltzcorr = 1./( 1. - np.exp( -planck*clight*vibfreq/(boltzmann*temp) ) )
    lasercorr = (laserfreq-vibfreq)**4/vibfreq
    prefactor = 2*(np.pi**2)*planck/(45.*clight)
    crsection = prefactor*lasercorr*boltzcorr*s
    return crsection



