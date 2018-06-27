
import numpy as np
from crewp.cuconv.constants_si import boltzmann
from crewp.cuconv.uconv import joule2ev

def gaussian(x, x0, sigma):
    return 1./(sigma*np.sqrt(2.*np.pi)) *\
            np.exp( -.5 * ((x-x0)/sigma)**2  )

def slater(x, x0, sigma):
    zeta = 1./sigma
    return np.exp(-zeta*abs(x-x0)) * zeta / 2.

def fermi(en, mu, temp):
    '''
    Fermi-Dirac distribution.
    Units:
        en: Energy, eV, because electron is the most common fermion.
        mu: chemical potential, (offset of energy), eV.
        temp: Temperature, Kelvin.
    '''
    return 1./ ( np.exp( (en-mu)/(boltzmann*joule2ev*temp) ) + 1. )
