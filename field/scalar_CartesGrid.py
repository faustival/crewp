
import sys
import numpy as np
from scipy.integrate import simps
from crewp.gaus_chem.cube import read_cube

class ScalarField:
    '''
    Applies to e.g., charge-density, potentials, 
    '''
    def __init__( 
            self, 
            data3d=None,   # 3d-array
            cell=None, # 3*3 array, vectors of cell 
            delta_grid=None, # 3*3 array, vectors of grid increament
            cell_origin=None, # 1*3 array, origin coordinate
            inpfname=None, # 
            ):
        if inpfname:
            self.cell_origin, self.delta_grid, self.data3d = read_cube(inpfname)
        else:
            sys.exit('Input for ScalarField, not implemented.')
        self.gridshape = self.data3d.shape

    def test_cartesgrid(self):
        '''
        Determine if grid is Cartesian.
        by evaluate ``cell`` or ``delta_grid`` is diagonal.
        '''
        m = self.delta_grid
        self.t_cartesgrid = ( np.count_nonzero(m - np.diag(np.diagonal(m))) == 0 )
        return self.t_cartesgrid

    def get_cartesgrid_arry(self):
        if self.test_cartesgrid():
            dx, dy, dz = np.diagonal(self.delta_grid)
            self.cartesgrid_arry = []
            for i, dl in enumerate( [dx, dy, dz] ):
                ng = self.gridshape[i]
                l0 = self.cell_origin[i]
                grid_arry = l0 + dl*np.arange(ng) 
                self.cartesgrid_arry.append(grid_arry)
        return self.cartesgrid_arry

    def get_avg2d(self, axis):
        '''
        Average through axis.
        '''
        avg2d = np.mean(self.data3d, axis=axis)
        return avg2d

