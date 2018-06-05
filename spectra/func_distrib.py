
import numpy as np

def gaussian(x, x0, sigma):
    return 1./(sigma*np.sqrt(2.*np.pi)) *\
            np.exp( -.5 * ((x-x0)/sigma)**2  )

def slater(x, x0, sigma):
    zeta = 1./sigma
    return np.exp(-zeta*abs(x-x0)) * zeta / 2.
