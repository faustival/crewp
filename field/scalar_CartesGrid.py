
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
            data3d=None, # 3d-array,
            cell=None, # 3*3 array, vectors of cell 
            grid_measure=None, # 3*3 array, vectors of grid increament
            delta_grid=None, # 1*3 array, (dx, dy, dz)
            cell_origin=None, # 1*3 array, (x0, y0, z0)
            inptype=None, # raw input, or file type 'cube'...
            inpfname=None, # 
            ):
        '''
        Dealing with types of input:
        '''
        if inptype=='cube' and inpfname:
            self.cell_origin, self.grid_measure, self.data3d = read_cube(inpfname)
        else:
            sys.exit('Crewp:ScalarField: Input for ScalarField, not implemented.')
        '''
        Case: get ``delta_grid`` from ``grid_measure`` matrix.
        '''
        if (not hasattr(self, 'delta_grid')) and hasattr(self, 'grid_measure'):
            if np.count_nonzero(self.grid_measure - np.diag(np.diagonal(self.grid_measure))) != 0 : # test if grid_measure diagonal.
                sys.exit('Crewp:ScalarField: Non-Cartesian grid of ScalarField, not implemented.')
            else:
                self.delta_grid = np.diagonal(self.grid_measure)
        self.gridshape = self.data3d.shape

    def get_grid_arrys(self):
        '''
        Calculate grid arrays from increaments ``delta_grid``
        Return a list of grid arrays, length may not be equal.
        [ 
            (x_0, x_1, ... x_nx),  
            (y_0, y_1, .... y_ny),  
            (z_0, z_1, ..... z_nz),  
        ]
        '''
        self.grid_arry = []
        for i, dl in enumerate( self.delta_grid ):
            ng = self.gridshape[i]
            l0 = self.cell_origin[i]
            grid_arry = l0 + dl*np.arange(ng) 
            self.grid_arry.append(grid_arry)
        return self.grid_arry

    def get_avg2d(self, axis):
        '''
        Average through axis.
        '''
        avg2d = np.mean(self.data3d, axis=axis)
        return avg2d

    def get_avg1d(self, axes):
        '''
        Average through axes.
        '''
        avg2d = np.mean(self.data3d, axis=max(axes))
        avg1d = np.mean(avg2d, axis=min(axes))
        return avg1d
