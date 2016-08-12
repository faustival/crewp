
'''
Detailed description of (A)XSF file, see official manual:
http://www.xcrysden.org/doc/XSF.html
'''

def wrt_anim_fixcell(primvec, atomlist, anim_coords, axsfname='anim_fixcell.axsf', ):
    axsf = open(axsfname, 'w')
    # write the header
    axsf.write( '{:s} {:d}'.format('ANIMSTEPS ', len(anim_coords))+'\n' )
    axsf.write( 'CRYSTAL\n' )
    # write primitive cell vectors
    axsf.write( 'PRIMVEC\n' )
    for i in range(3):
        axsf.write( '   '+' '.join( '{:13.8f}'.format(entry) for entry in primvec[i] )+'\n' )
    # write animation
    for i_step, atomvecs in enumerate(anim_coords, 1):
        axsf.write( '{:s} {:d}'.format('PRIMCOORD', i_step)+'\n' )
        axsf.write( '   {:d}    {:d}'.format(len(atomvecs), 1)+'\n' )
        for i_atom, vec in enumerate(atomvecs):
            axsf.write( '   {:2s} '.format(atomlist[i_atom]) + \
                        ' '.join( '{:13.8f}'.format(entry) for entry in vec ) + \
                        '\n' )
    axsf.close()



