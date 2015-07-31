#! /usr/bin/env python

from ase.lattice import surface

def wrtcrds(crds, oupf, tag):
    '''
    crds: coordinate, n*3 array
    oupf: output file
    '''
    oupf.write('\n' + tag + '\n')
    for crd in crds:
        oupf.write(''.join('%12.7f'%x for x in crd) + '\n') 

def shiftz(crds, shift):
    for coord in crds:
        coord[2] = coord[2] + shift
    return crds

def shift2center(coords):
    # shift center layer to 0
    shift_center = (coords[0][2] + coords[-1][2])/2.
    coords = shiftz(coords, -shift_center)
    return coords


slab = surface.fcc111('Ag', size=(1,1,7), a=4.20, vacuum=0.0)

coords = slab.get_positions()
cell = slab.get_cell()

# build the vacuum
coords = shiftz(coords, 20.)
cell[2][2] += 40.

# shift z-0 to slab center
#coords = shift2center(coords)

coord_tag = 'atomic coordinates:'
cell_tag = 'lattice cell vectors:'


print coords
print cell

oup = open('samplecoord.log', 'w')
wrtcrds(coords, oup, coord_tag)
wrtcrds(cell, oup, cell_tag)
oup.close()





