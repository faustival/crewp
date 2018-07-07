#! /usr/bin/env python3

import sys
from crewp.vasp.outcar import Outcar
from crewp.vasp.poscar import Poscar
from crewp.xcrysden.xcrysf import wrt_anim

if len(sys.argv) < 2:
    outcarfname = 'OUTCAR'
else:
    outcarfname = sys.argv[1]

print('Reading VASP OUTCAR filetype, ', outcarfname)
outcar = Outcar(outcarfname)
outcar.read_latvecs()
outcar.auto_creep()

# get selective dynamics constraint in POSCAR
poscar = Poscar('POSCAR')
constraint = poscar.get_constraint()
constraint[ constraint ] == 0.
outcar.anim_vec6d[:,:,3:] *= constraint

# scale force vector if need
if 1 <= outcar.ibrion <= 3: # relaxation
    outcar.anim_vec6d[:,:,3:] *= 1.#/27.2 
    axsfname = 'anim_rlx.axsf'
elif outcar.ibrion == 0: # molecular dynamics
    outcar.anim_vec6d[:,:,3:] *= 1.#/27.2 
    axsfname = 'anim_md.axsf'
elif 5 <= outcar.ibrion <= 8: # vibrational frequencies
    outcar.anim_vec6d[:,:,3:] *= 1./50. 
    axsfname = 'anim_vib.axsf'

wrt_anim( 
          primvec = outcar.latvecs,
          anim_coords = outcar.anim_vec6d,
          atomlist = outcar.atomlist,
          axsfname = axsfname,
        )

