#! /usr/bin/python3

import sys
from crewp.vasp.parsexml import ParseXML
from crewp.io.array import wrt_2darry, wrt_3darry

if len(sys.argv) < 2:
    xmlfname = 'vasprun.xml'
else:
    xmlfname = sys.argv[1]

print('Reading VASP XML output, ', xmlfname)
xmlf = ParseXML(xmlfname)
atomlist = xmlf.get_atomlist()

# bornchrg( natoms, coord3, field3 )
bornchrg = xmlf.get_3dvarray('//calculation/array[@name="born_charges"]/set')

wrt_3darry(bornchrg, 'bornchrg')


