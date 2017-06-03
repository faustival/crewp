#! /usr/bin/env python3

import sys
from crewp.vasp.outcar import Outcar
from crewp.xcrysden.xcrysf import wrt_anim

if len(sys.argv) < 2:
    inpfname = 'OUTCAR'
else:
    inpfname = sys.argv[1]

print('Reading VASP OUTCAR filetype, ', inpfname)
outcar_obj = Outcar(inpfname)
outcar_obj.get_latvecs()
outcar_obj.auto_creep()

# scale force vector if need
if 1 <= outcar_obj.ibrion <= 3: # relaxation
    outcar_obj.anim_vec6d[:,:,3:] *= 1./27.2 
    axsfname = 'anim_rlx.axsf'
elif outcar_obj.ibrion == 0: # molecular dynamics
    outcar_obj.anim_vec6d[:,:,3:] *= 1./27.2 
    axsfname = 'anim_md.axsf'
elif 5 <= outcar_obj.ibrion <= 8: # vibrational frequencies
    outcar_obj.anim_vec6d[:,:,3:] *= 1./50. 
    axsfname = 'anim_vib.axsf'

wrt_anim( 
          primvec = outcar_obj.latvecs,
          anim_coords = outcar_obj.anim_vec6d,
          atomlist = outcar_obj.atomlist,
          axsfname = axsfname,
        )

