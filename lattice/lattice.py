
import numpy as np

def frac2cart(frac_coord, lat_vec):
    return frac_coord.dot(lat_vec)

def cell_volume(lat_vec):
    return abs(np.linalg.det(lat_vec))
