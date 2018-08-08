
import numpy as np
from crewp.io.array import wrt_2darry

'''
Detailed description of (A)XSF file, see official manual:
http://www.xcrysden.org/doc/XSF.html
'''

def wrt_anim(primvec, anim_coords, atomlist, axsfname='anim_xcrys.axsf', ):
    '''
    Write as fix cell if primvec is input as 2d-array,
        else iterate 1st index of primvec (3d-array) to variable cell.
    '''
    fixcell = ( len( np.shape(primvec) ) == 2 ) # if primvec input as 2d-array
    natoms = anim_coords.shape[1] # number of atoms
    with open(axsfname, 'w', ) as axsf:
        axsf.write( '{:s} {:d}'.format('ANIMSTEPS ', len(anim_coords))+'\n' )
        axsf.write( 'CRYSTAL\n' )
        if fixcell: # write fix lattice cell 
            wrt_2darry(primvec, title='PRIMVEC', f=axsf)
        for i_step, anim_step in enumerate(anim_coords): # write animation
            if not fixcell:
                title_latvec = '{:s} {:d}'.format('PRIMVEC', i_step+1)
                wrt_2darry(primvec[i_step], title=title_latvec , f=axsf)
            title_coord = '{:s} {:d}'.format('PRIMCOORD', i_step+1)+'\n' \
                          + '   {:d}    {:d}'.format(natoms, 1)
            wrt_2darry(anim_step, title=title_coord, rowtags=atomlist, f=axsf, )
            axsf.write( '\n' )



