
import numpy as np
from crewp.io.array import wrt_2darry

'''
Detailed description of (A)XSF file, see official manual:
http://www.xcrysden.org/doc/XSF.html
'''

def wrt_anim(atomlist, anim_coords, primvec=None, axsfname='anim_xcrys.axsf'):
    '''
    Write as fix cell if primvec is input as 2d-array,
        else iterate 1st index of primvec (3d-array) to variable cell.
    if primvec given, structure as crystal, else as molecule
    '''
    if primvec is not None: 
        fixcell = ( len( np.shape(primvec) ) == 2 ) # if primvec input as 2d-array
    natom = len(atomlist) # number of atoms
    with open(axsfname, 'w', ) as axsf:
        axsf.write( '{:s} {:d}'.format('ANIMSTEPS ', len(anim_coords))+'\n' )
        if primvec is not None: 
            axsf.write( 'CRYSTAL\n' )
            if fixcell: # write fix lattice cell 
                wrt_2darry(primvec, title='PRIMVEC', f=axsf)
        for i_step, anim_step in enumerate(anim_coords): # write animation
            if primvec is not None:
                if not fixcell:
                    title_latvec = '{:s} {:d}'.format('PRIMVEC', i_step+1)
                    wrt_2darry(primvec[i_step], title=title_latvec , f=axsf)
                title_coord = '{:s} {:d}'.format('PRIMCOORD', i_step+1)+'\n' \
                              + '   {:d}    {:d}'.format(natom, 1)
            else:
                title_coord = '{:s} {:d}'.format('ATOMS', i_step+1)+'\n'
            wrt_2darry(anim_step, f=axsf, lmargin=3, title=title_coord, rowtags=atomlist, )
            axsf.write( '\n' )

