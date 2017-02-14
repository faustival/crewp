#! /usr/bin/python3

import sys
from crewp.vasp.parsexml import ParseXML
from crewp.xcrysden.xcrysf import wrt_anim

if len(sys.argv) < 2:
    xmlfname = 'vasprun.xml'
else:
    xmlfname = sys.argv[1]

print('Reading VASP XML output, ', xmlfname)
xmlf = ParseXML(xmlfname)
xmlf.auto_creep()

'''
# scale force vector if need
if 1 <= outcar_obj.ibrion <= 3:
    outcar_obj.anim_vec6d[:,:,3:] *= 1./27.2 
    axsfname = 'anim_rlx.axsf'
elif 5 <= outcar_obj.ibrion <= 8:
    outcar_obj.anim_vec6d[:,:,3:] *= 1./50. 
    axsfname = 'anim_vib.axsf'

wrt_anim_fixcell( axsfname = axsfname,
                  primvec = outcar_obj.latvecs,
                  atomlist = outcar_obj.atomlist,
                  anim_coords = outcar_obj.anim_vec6d,
                )
'''
