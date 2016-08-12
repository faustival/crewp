#! /usr/bin/python3

import sys
from crewp.vasp.outcar import Outcar
from crewp.xcrysf import wrt_anim_fixcell

def scale_anim_force(anim_coords, scale=1./27.2):
    for atomvecs in anim_coords:
        for vec in atomvecs:
            for i in range(3,6):
                vec[i] = vec[i]*scale
    return anim_coords

if len(sys.argv) < 2:
    inpfname = 'OUTCAR'
else:
    inpfname = sys.argv[1]

print('Reading VASP OUTCAR filetype, ', inpfname)
outcar_obj = Outcar(inpfname)
outcar_obj.get_latvecs()
outcar_obj.auto_creep()

# scale force vector if need
if 1 <= outcar_obj.ibrion <= 3:
    outcar_obj.anim_vec6d = scale_anim_force(outcar_obj.anim_vec6d, 1./27.2)
    axsfname = 'anim_rlx.axsf'
elif 5 <= outcar_obj.ibrion <= 8:
    axsfname = 'anim_vib.axsf'

wrt_anim_fixcell( axsfname = axsfname,
                  primvec = outcar_obj.latvecs,
                  atomlist = outcar_obj.atomlist,
                  anim_coords = outcar_obj.anim_vec6d,
                )

