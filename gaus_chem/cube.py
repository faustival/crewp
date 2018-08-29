
import sys
import numpy as np
from crewp.cuconv.uconv import bohr2ang
from crewp.io.array import read_2darry

'''
http://gaussian.com/cubegen/
'''

def read_cube(cubefname):
    '''
    r0: origin coordinate of grid, 1*3 array, [x0, y0, z0]
    ngrid: 1*3 array, [nx, ny, nz]
    dr: grid shift along 3 vectors, 3*3 array, [ [dxvec], [dyvec], [dzvec] ], diagonal if grid is Cartesian (rectangular and extended along x,y,z axis)
    volumdata: reshape as ngrid 
    '''
    with open(cubefname, 'r') as f:
        f.readline() # 1st comment line
        f.readline() # 2nd comment line
        natom, x0, y0, z0 = f.readline().split()
        natom, x0, y0, z0 = int(natom), float(x0)*bohr2ang, float(y0)*bohr2ang, float(z0)*bohr2ang, 
        r0 = np.array([x0, y0, z0])
        ng_dr = read_2darry(f, nrow=3, typefunc='str')
        ngrid = ng_dr[:,0].astype(int)
        dr = ng_dr[:,1:].astype(float)*bohr2ang
        for i in range(natom):
            f.readline() # atomic coordinates
        volumdata = np.fromfile(f, count=np.prod(ngrid), sep=' ')
        volumdata = volumdata.reshape(ngrid)
        return r0, dr, volumdata

