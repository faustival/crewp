#! /usr/bin/python3

import sys
from qescripts.vasp.outcar import Outcar
from qescripts.xcrysf import wrt_anim_fixcell

if len(sys.argv) < 2:
    inpfname = 'OUTCAR'
else:
    inpfname = sys.argv[1]

print('Reading VASP OUTCAR filetype, ', inpfname)

outcar_obj = Outcar(inpfname)
outcar_obj.get_latvecs()
outcar_obj.auto_creep()

wrt_anim_fixcell( axsfname='anim_fixcell.axsf',
                  primvec = outcar_obj.latvecs,
                  atomlist = outcar_obj.atomlist,
                  anim_coords = outcar_obj.anim_vec6d,
                )

