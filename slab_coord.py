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


oup = open('au110samplecoord.log', 'w')
au_slab = surface.fcc110('Au', size=(1,1,30), a=4.16, vacuum=0.0)

coords = au_slab.get_positions()
cell = au_slab.get_cell()

coord_tag = 'atomic coordinates:'
cell_tag = 'lattice cell vectors:'

print coords
print cell

wrtcrds(coords, oup, coord_tag)
wrtcrds(cell, oup, cell_tag)




