#! /usr/bin/python3

import sys
from qescripts.vasp.outcar import Outcar

if len(sys.argv) < 2:
    inpfname = 'OUTCAR'
else:
    inpfname = sys.argv[1]

print('Reading VASP OUTCAR filetype, ', inpfname)

outcar_obj = Outcar(inpfname)
outcar_obj.get_latvecs()
outcar_obj.auto_creep()



